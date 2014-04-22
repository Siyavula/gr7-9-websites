var filelists = {'natural-sciences-gr7':
                    ['tableofcontents.html',
                    'gr7-ll-01.html',
                    'gr7-ll-02.html',
                    'gr7-ll-03.html',
                    'gr7-ll-04.html',
                    'gr7-ll-glossary.html',
                    'gr7-mm-01.html',
                    'gr7-mm-02.html',
                    'gr7-mm-03.html',
                    'gr7-mm-04.html',
                    'gr7-mm-glossary.html',
                    'gr7-ec-01.html',
                    'gr7-ec-02.html',
                    'gr7-ec-03.html',
                    'gr7-ec-04.html',
                    'gr7-ec-05.html',
                    'gr7-ec-06.html',
                    'gr7-ec-glossary.html',
                    'gr7-eb-01.html',
                    'gr7-eb-02.html',
                    'gr7-eb-03.html',
                    'gr7-eb-glossary.html'],

                'natuurwetenskappe-gr7': 
                    ['inhoudsopgawe-afr.html',
                    'gr7-ll-01-afr.html',
                    'gr7-ll-02-afr.html',
                    'gr7-ll-03-afr.html',
                    'gr7-ll-04-afr.html',
                    'gr7-ll-woordelys-afr.html',
                    'gr7-mm-01-afr.html',
                    'gr7-mm-02-afr.html',
                    'gr7-mm-03-afr.html',
                    'gr7-mm-04-afr.html', 
                    'gr7-ec-01-afr.html',
                    'gr7-ec-02-afr.html',
                    'gr7-ec-03-afr.html',
                    'gr7-ec-04-afr.html',
                    'gr7-ec-05-afr.html',
                    'gr7-ec-06-afr.html',
                    'gr7-ec-woordelys-afr.html',
                    'gr7-eb-01-afr.html',
                    'gr7-eb-02-afr.html',
                    'gr7-eb-03-afr.html',
                    'gr7-eb-woordelys-afr.html'],

                'natural-sciences-gr8':
                    ['tableofcontents.html',
                    'gr8-ll-01.html',
                    'gr8-ll-02.html',
                    'gr8-ll-03.html',
                    'gr8-ll-glossary.html',
                    'gr8-mm-01.html',
                    'gr8-mm-02.html',
                    'gr8-mm-03.html',
                    'gr8-mm-glossary.html',
                    'gr8-ec-01.html',
                    'gr8-ec-02.html',
                    'gr8-ec-03.html',
                    'gr8-ec-04.html',
                    'gr8-ec-glossary.html',
                    'gr8-eb-01.html',
                    'gr8-eb-02.html',
                    'gr8-eb-03.html',
                    'gr8-eb-glossary.html'],

                'natuurwetenskappe-gr8':
                    ['inhoudsopgawe-afr.html',
                    'gr8-ll-01-afr.html',
                    'gr8-ll-02-afr.html',
                    'gr8-ll-03-afr.html',
                    'gr8-ll-woordelys-afr.html',
                    'gr8-mm-01-afr.html',
                    'gr8-mm-02-afr.html',
                    'gr8-mm-03-afr.html',
                    'gr8-mm-woordelys-afr.html',
                    'gr8-ec-01-afr.html',
                    'gr8-ec-02-afr.html',
                    'gr8-ec-03-afr.html',
                    'gr8-ec-04-afr.html',
                    'gr8-ec-woordelys-afr.html',
                    'gr8-eb-01-afr.html',
                    'gr8-eb-02-afr.html',
                    'gr8-eb-03-afr.html',
                    'gr8-eb-woordelys-afr.html']
};


$( document ).ready(function() {

    var addNavLinks = function(navelement){
        // Add links to the next and previous buttons.
        var thispage = location.pathname.split('/');
        var filename = thispage[thispage.length-1];
        var currentfilelist;
        var nextfile;
        var prevfile;
        var grade;
        var strand;
        var chap;


        grade = filename.split('-')[0];
        strand = filename.split('-')[1];

        // if it is not the table of contents.
        if (filename.indexOf('tableofcontents') === -1 && filename.indexOf('inhoudsopgawe-afr') === -1 ){
            chap = filename.split('-')[2];
        }
        // if it is the table of contents
        else {
            grade = thispage[2];
        }

        // get the correct file list from the variable
        if (location.pathname.indexOf('natural-sciences') !== -1){
            currentfilelist = filelists['natural-sciences-' + grade];
        }
        else if (location.pathname.indexOf('mathematics') !== -1){
            currentfilelist = filelists['mathematics-' + grade];
        }
        else if (location.pathname.indexOf('technology') !== -1){
            currentfilelist = filelists['technology-' + grade];
        }
        else if (location.pathname.indexOf('natuurwetenskappe') !== -1){
            currentfilelist = filelists['natuurwetenskappe-' + grade];
        }
        else if (location.pathname.indexOf('wiskunde') !== -1){
            currentfilelist = filelists['wiskunde-' + grade];
        }
        else if (location.pathname.indexOf('tegnologie') !== -1){
            currentfilelist = filelists['tegnologie-' + grade];
        }
        // set the next and previous files' links
        for (var i=0; i < currentfilelist.length-1; i++) {
            // if the current file is not the first or last in a chapter
            if (filename == currentfilelist[i] && i !== 0 && i !== currentfilelist.length-1){
                nextfile = currentfilelist[i+1];
                prevfile = currentfilelist[i-1];
            }
            // if the current file is the table of contents, set previous to inactive and only set next.
            else if (i == 0){
                nextfile = currentfilelist[i+1];
                prevfile = '#';
            }
            else if (i == currentfilelist.length-1){
                nextfile = '#';
                prevfile = currentfilelist[i-1];
            }
        }

        // set the link for the next file
        $('a.next').each(function(){
            $(this).prop('href', nextfile);                
        });
        $('a.previous').each(function(){
            $(this).prop('href', prevfile);                
        });
    }

    $('ul.pager').each(function(){
        addNavLinks($(this))      
    });
});
