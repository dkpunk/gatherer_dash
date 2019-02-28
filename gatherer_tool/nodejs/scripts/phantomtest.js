var phantom = require('phantom');

phantom.create().then(function(ph) {
  ph.createPage().then(function(page) {
    page.open('http://velocity.support.envestnet.cloud/search-results?searchString=172.18.22.121').then(function(status) {
      console.log(status);
      page.property('content').then(function(content) {
        console.log(content);
        page.close();
        ph.exit();
      });
    });
  });
});
