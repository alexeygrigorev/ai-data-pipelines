## Getting a GitHub API Key

To access the GitHub API, you need a personal access token:

1. Go to [GitHub Settings](https://github.com/settings/profile).
2. Click Developer settings > Personal access tokens > Fine-grained personal access tokens.
3. Click Generate new token.
4. Token name = "ai-bootcamp", access = public. no extra scopes if we want to read only public data (issues, PRs, etc)
5. Click Generate token and copy the token.
6. Save it to `GITHUB_API_TOKEN` env variable, e.g. in your `.envrc`.


Keep your token secure and do not share it publicly.

Pagination in github:

```
# https://api.github.com/repos/pydantic/pydantic-ai/issues

# $ curl -I https://api.github.com/repos/pydantic/pydantic-ai/issues
# ...
# link: <https://api.github.com/repositories/818331198/issues?after=...%3D%3D&per_page=30&page=2>; rel="next"
# -> HeaderLinkPaginator
# see here https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api?apiVersion=2022-11-28

```


TODO DLT what is it 

extra benefit: caching
(no need to use cache)