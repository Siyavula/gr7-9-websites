var toggleAfrEng = function(pathname) {
    // check if pathname contains -afr.html or not.
    // If it does, return the pathname without -afr else add it and return
    var newpathname = '';

    if (pathname.indexOf('-afr.html') == -1) {
        // -afr is not in the path name
        newpathname = pathname.replace('.html', '-afr.html')
    }
    else {
        // -afr is in the path name
        newpathname = pathname.replace('-afr.html', '.html')
    }

    return newpathname;
}


$( document ).ready(function() {
    $('div.language-toggle').on('click', function(){
        var newpage = toggleAfrEng(location.pathname);
        open(newpage, '_self');
    });
});
