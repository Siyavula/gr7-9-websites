//Executes your code when the DOM is ready.  Acts the same as $(document).ready().
$(function() {
    
      

    //Calls the tocify method on your HTML div.
    $("#toc").tocify({
       selectors: 'h1,h2,h3,h4'
    });
});
