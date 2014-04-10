function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}


$( document ).ready(function() {

    var addNavLinks = function(navelement){

        var thispage = location.pathname.split('/');
        var filename = thispage[thispage.length-1];

        // get grade, strand and chapter number
        var grade;
        var strand;
        var chap;
        grade = filename.split('-')[0];
        strand = filename.split('-')[1];
        chap = filename.split('-')[2].split('.')[0];
        console.log(grade, strand, chap);


        var strandorder = new Array();
        strandorder[0] = 'tableofcontents';
        strandorder[1] = 'll';
        strandorder[2] = 'mm';
        strandorder[3] = 'ec';
        strandorder[4] = 'eb';

        // get the name of the next file in the correct order
        var nextfile;

        if (chap == 'glossary') {
            for (var i=0; i<5; i++) {
                if (strandorder[i] == strand && i < 4) {
                    nextfile = grade + '-' + strandorder[i+1] + '-' + '01.html';
                    break;
                }
                if (i == 4) {
                    nextfile = "#";
                }
            }
        }
       else {
            // check if the next file exists
            nextchap = +chap + 1
            nextfile = grade + '-' + strand + '-0' + nextchap + '.html';
            if (UrlExists(location.pathname.replace(filename, nextfile))){
                // the url exists
            }
            else {
                // the next one must be the glossary
                nextfile = grade + '-' + strand + '-glossary.html';
            }
        }
        
        // set the link for the next file
        $('a.next').each(function(){
            $(this).prop('href', nextfile);                
        });


//
//  Now lets look for the previous file in order
//
        var prevfile;
        

    }

    $('ul.pager').each(function(){
        addNavLinks($(this))      
    });
});
