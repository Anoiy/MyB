function search_click() {
    var keywords = $('#search').val();
    if (keywords == '') {
        return 0;
    }
    var request_url = '/article/search?keywords=' + keywords;
    window.location.href = request_url;
}