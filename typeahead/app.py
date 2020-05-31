import os
from flask import request
from typeahead import app
from typeahead.index import SearchIndex

max_heap_size = app.config.get("MAX_HEAP_SIZE")
max_prefix_size = app.config.get("MAX_PREFIX_SIZE")
version = app.config.get("VERSION")
data_dir = app.config.get("INDEX_DIR")

searchIndex = SearchIndex(max_heap_size, max_prefix_size)


@app.before_first_request
def load_index():
    searchIndex.load(data_dir, version)


@app.route("/")
def info():
    return searchIndex.info()


@app.route("/search/<prefix>")
def autocomplete(prefix):
    return str(searchIndex.search(prefix))


@app.route("/healthcheck")
def healthcheck():
    return "healthy"


@app.route("/admin/index/reload", methods=["POST"])
def reload_index():
    pass


@app.route("/admin/index/<prefix>", methods=["POST", "DELETE"])
def update_index(prefix):
    """
    Content-type : application/json
    Body:
        { prefix : list of words to update }
    """
    content = request.json
    update_words = content[prefix][:max_heap_size]
    # update
    if request.method == "POST":
        if update_words:
            # 0 count indicates manual appending
            searchIndex.index[prefix][:len(update_words)] = [(0, word) for word in update_words]
        else:
            searchIndex.index[prefix] = []  # remove all
    # delete certain words from index
    else:
        searchIndex.index[prefix] = [item for item in searchIndex.index[prefix] if item[1] not in update_words]

    # file write
    with open(os.path.join(data_dir, "update.bin"), "ab") as f:
        encoded = prefix.encode()
        f.write(bytes([len(encoded)]) + encoded + bytes([len(update_words)]))
        for i, (count, word) in enumerate(searchIndex.index[prefix]):
            encoded = word.encode()
            f.write(bytes([len(encoded)]) + count.to_bytes(4, byteorder="little") + encoded)

    return str(update_words)
