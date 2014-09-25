var toggleAfrEng = function(pathname) {
    // check if pathname contains -afr.html or not.
    // If it does, return the pathname without -afr else add it and return
    var newpathname = '';
    var transTable = [['natural-sciences', 'natuurwetenskappe'], ['mathematics','wiskunde'], ['technology', 'tegnologie'], ['tableofcontents','inhoudsopgawe'], ['downloads', 'aflaaibares'], ['about' ,'oorons']]

    if (pathname.indexOf('-afr.html') == -1) {
        // -afr is not in the path name
        newpathname = pathname.replace('.html', '-afr.html')

        // do some other translations from english to afrikaans
        for (var i=0; i < transTable.length; i++){
            var eng = transTable[i][0];
            var afr = transTable[i][1];
            var find = eng;
            var re = new RegExp(find, 'g');
            newpathname = newpathname.replace(re, afr);
        }
    }
    else {
        // -afr is in the path name
        newpathname = pathname.replace('-afr.html', '.html')
        // do some other translations from afrikaans to english
        for (var i=0; i < transTable.length; i++){
            var eng = transTable[i][0];
            var afr = transTable[i][1];
            var find = afr;
            var re = new RegExp(find, 'g');
            newpathname = newpathname.replace(re, eng);
        }
    }



    return newpathname;
}


$( document ).ready(function() {
    $('div.language-toggle').on('click', function(){
        var newpage = toggleAfrEng(location.pathname);
        open(newpage, '_self');
    });
});
