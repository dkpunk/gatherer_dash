var page = require('webpage').create();
page.open("http://velocity.support.envestnet.cloud/search-results?searchString=172.18.22.121", function (status)
{
    if (status !== 'success') 
    {
        console.log('FAIL to load the address');            
    } 
    else 
    {
        console.log('Success in fetching the page');
        console.log(page.content);
    }
    phantom.exit();
});
