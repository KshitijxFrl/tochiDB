from groq import Groq
from .utility import query_cache, normalize_query, update_query_cache
from . import utility


def natural_to_sql(prompt, key):

    normalized_query = normalize_query(prompt)
    
    #! Stage first checking that the query is in the chache if yes it will return the appropriate query for the natural query 
    if normalized_query in utility.query_cache:
        print("Query found in the cache")
        return utility.query_cache[normalized_query]   

    #! If query dont exist in the cache it will gnerate it using the AI of your choise.
    client = Groq(api_key= key)
    chat_completion = client.chat.completions.create(
        messages=[  
            {
                "role": "system",
                "content": """You are a Postgres SQL master. Return only the correct SQL query with no extra text. 
                            - **Use placeholders (`%s`)** only for `INSERT`, `UPDATE`, and `WHERE` conditions.
                            - **Do NOT use placeholders** for `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`, `SHOW`, or `DESCRIBE` queries.
                            - Ensure SQL syntax is valid.
                            - Return just the query—no explanations or formatting.
                            """
            },

            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,

        max_completion_tokens=1024,

        top_p=1,

        stop=None,

        stream=False,
    )

    result_query = chat_completion.choices[0].message.content

    update_query_cache(normalized_query, result_query)

    return result_query


def natural_to_sql2(prompt, key):

    normalized_query = normalize_query(prompt)

    #! Stage first checking that the query is in the chache if yes it will return the appropriate query for the natural query 
    if normalized_query in query_cache:
        print("Query found in the cache")
        return query_cache[normalized_query]   

    #! If query dont exist in the cache it will gnerate it using the AI of your choise.
    client = Groq(api_key= key)
    chat_completion = client.chat.completions.create(
        messages=[
            
            {
                "role": "system",
                "content": "you are a Postgres SQL master and will provide the correct query for the prompt. Return only the query which is asked nothing extra just to the point. [Remove ```sql (query) ```  from the out put and give just the query]. Ignore every other request which does't related to generating a query or database manupulation (when encounterning that situation just return REQUEST IS NOT VALID)"
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,

        max_completion_tokens=1024,

        top_p=1,

        stop=None,

        stream=False,
    )

    result_query = chat_completion.choices[0].message.content

    update_query_cache(normalized_query, result_query)
    #query_cache[normalized_query] = result_query

    return result_query

if __name__ == "__main__":
    sample_prompt = "Return all user with 50000 anaual income for all user."
    result = natural_to_sql(sample_prompt)
    print(result)