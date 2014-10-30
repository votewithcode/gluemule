
##github
### Get Repos
```curl -XGET https://api.github.com/orgs/cfpb/repos```

### Get Issues
```curl -XGET https://api.github.com/repos/cfpb/issues```

### Get rate limit
```curl https://api.github.com/rate_limit```


##elasticsearch

###Add a doc and assign and id

```curl -XPOST 'http://localhost:9200/gluemule/org/' -d '{"name": "cfpb","url": "https://github.com/cfpb","location": "Washington, D.C.","blog": "http://cfpb.github.io","home_page": "http://www.consumerfinance.gov"}'```

### Remove a doc
```curl -XDELETE 'http://localhost:9200/gluemule/org/1'``` 

### Query
```curl -XGET 'http://localhost:9200/gluemule/org/1'```

```curl -XGET 'http://localhost:9200/_search?q=cfpb'```

### Remove the entire index
```curl -XDELETE 'http://localhost:9200/gluemule```

### Adds an org
ORG=$(curl https://api.github.com/orgs/cfpb); curl -XPOST 'http://localhost:9200/gluemule/org/' -d $ORG
