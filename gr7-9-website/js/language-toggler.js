var toggleAfrEng = function(pathname) {
    // check if pathname contains -afr.html or not.
    // If it does, return the pathname without -afr else add it and return
    var newpathname = '';
    var transTable = [['natural-sciences', 'natuurwetenskappe'], ['mathematics','wiskunde'], ['technology', 'tegnologie'], ['tableofcontents','inhoudsopgawe']]

    if (pathname.indexOf('-afr.html') == -1) {
        // -afr is not in the path name
        newpathname = pathname.replace('.html', '-afr.html')

        // do some other translations from english to afrikaans
        for (var i=0; i < transTable.length; i++){
            var eng = transTable[i][0];
            var afr = transTable[i][1];
            newpathname = newpathname.replace(eng, afr);
        }
    }
    else {
        // -afr is in the path name
        newpathname = pathname.replace('-afr.html', '.html')
        // do some other translations from afrikaans to english
        for (var i=0; i < transTable.length; i++){
            var eng = transTable[i][0];
            var afr = transTable[i][1];
            newpathname = newpathname.replace(afr, eng);
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
