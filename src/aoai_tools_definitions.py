tools = [
    {
        "type": "function",
        "function": {
            "name": "bing_web_search",
            "description": '''Use this function to perform a search with the Bing Web Search API and its advanced search capabilities.
                    Input should be a well written search query adhering to advanced search keywords and their notation or additional API Query parameters as noted.
                    Use of advanced keyword formatting and additional keywords is encouraged to get the best results.''',
            "parameters": {  
                "type": "object",  
                "properties": {  
                    "query": {  
                        "type": "string",  
                        "description": '''The user's search query term. Supports advanced search keywords.
                            Search Operators and Their Uses:
                            - contains: Focuses on websites with links to specified file types.
                            Example: music contains:wma
                            - ext: Filters webpages with a specific filename extension.
                            Example: subject ext:docx
                            - filetype: Narrows search to webpages in a specified file format.
                            Example: subject filetype:pdf
                            - inanchor:, inbody:, intitle: Search for webpages with terms in the anchor, body, or title.
                            Example: inanchor:msn inbody:spaces inbody:magog
                            - ip: Finds sites hosted by a specific IP address.
                            Example: IP:207.46.249.252
                            - language: Filters webpages to a specific language.
                            Example: "antiques" language:en
                            - loc: or location: Returns webpages from a specified country or region.
                            Example: sculpture (loc:US OR loc:GB)
                            - prefer: Adds emphasis to a search term or operator.
                            Example: football prefer:organization
                            - site: Searches within a specified site or domain.
                            Example: "heart disease" (site:bbc.co.uk OR site:cnn.com)
                            - feed: Finds RSS or Atom feeds on a website.
                            Example: feed:football
                            - hasfeed: Locates webpages with RSS or Atom feeds on a site.
                            Example: site:www.nytimes.com hasfeed:football
                            - url: Verifies if a domain or web address is indexed by Bing.
                            Example: url:microsoft.com''',
                        "minLength": 1
                    },
                    "**kwargs": {
                        "type": "object",
                        "description": '''This reference outlines the query parameters available for Bing Web Search API requests, detailing their purpose, value types, and whether they are mandatory.
                                answerCount: Specifies the number of answers (e.g., webpages, images) to include in the response based on ranking. Type: Unsigned Integer, Required: No
                                cc: Sets a 2-character country code to determine the country for the search results. Type: String, Required: No
                                count: Determines the number of search results to return. Default is 10, maximum is 50. Type: UnsignedShort, Required: No
                                freshness: Filters search results by age (Day, Week, Month) or a specific date range. Type: String, Required: No
                                mkt: Specifies the market (country/region) for the search results. Type: String, Required: No
                                offset: Sets the number of search results to skip before returning results. Type: Unsigned Short, Required: No
                                promote: A list of answers to include in the response regardless of their ranking. Type: String, Required: No
                                q: The user's search query term. Type: String, Required: Yes
                                responseFilter: A list of answer types to include in the response. Type: String, Required: No
                                safeSearch: Filters content for adult material. Options are Off, Moderate, Strict. Type: String, Required: No
                                setLang: Sets the language for user interface strings. Type: String, Required: No
                                textDecorations: Determines if display strings include decoration markers. Type: Boolean, Required: No
                                textFormat: The type of markers to use for text decorations (Raw or HTML). Type: String, Required: No
                                '''
                    }
                },
                "required": ["query"]
            },
            "returns": {
                "type": "string",
                "description": "A table with the search results in the specified format or an error message, including additional details."
            },
        }
    }
]