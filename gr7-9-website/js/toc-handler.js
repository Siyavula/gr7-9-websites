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
                    'gr7-eb-glossary.html']};


$( document ).ready(function() {

    var addNavLinks = function(navelement){

        var thispage = location.pathname.split('/');
        var filename = thispage[thispage.length-1];
        var currentfilelist;
        var nextfile;
        var prevfile;
        // get grade, strand and chapter number
        var grade;
        var strand;
        var chap;
        grade = filename.split('-')[0];
        strand = filename.split('-')[1];

        console.log(filename);
        // if it is not the table of contents.
        if (filename.substring('tableofcontents') == -1){
            chap = filename.split('-')[2].split('.')[0];
        }
        // if it is the table of contents
        else {
            grade = thispage[2];
        }

        // get the correct file list from the variable
        if (location.pathname.substring('natural-sciences') !== -1){
            currentfilelist = filelists['natural-sciences-' + grade];
        }
        else if (location.pathname.substring('mathematics') !== -1){
            currentfilelist = filelists['mathematics-' + grade];
        }
        else {
            currentfilelist = filelists['technology-' + grade];
        }
        
        // set the next and previous files' links
        for (var i=0; i < currentfilelist.length; i++) {
            // if the current file is not the first or last in a chapter
            if (filename == currentfilelist[i] && i !== 0 && i !== currentfilelist.length-1){
                nextfile = currentfilelist[i+1];
                prevfile = currentfilelist[i-1];
                break;
            }
            // if the current file is the table of contents, set previous to inactive and only set next.
            else if (i == 0){
                nextfile = currentfilelist[i+1];
                prevfile = '#';
                break;
            }
            else {
                nextfile = '#';
                prevfile = currentfilelist[i-1];
                break;
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
