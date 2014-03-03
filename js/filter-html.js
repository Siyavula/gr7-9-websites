$(function() {
    var toc = $('#toc');
    var tocids = [];
    var currentTocId = 0;
    var headings = [];

    // get all heading elements that match the selectors
    $('.title').each(function(){
        if ($(this).parent().prop('class') == 'section'){
            headings.push($(this));
        }
    });



    for (var i=0; i < headings.length; i++){
        var a = $('<a>' + headings[i].text() + '</a>');
        a.attr('href', '#toc-id-' + currentTocId);
        a.addClass(headings[i].prop('tagName'));

        var li = $('<p></p>');
        li.append(a);
        headings[i].prop('id', 'toc-id-' + currentTocId);
        currentTocId += 1;
        console.log(headings[i].text());
        toc.append(li);
    }


    $('#toc').append(toc);


});
