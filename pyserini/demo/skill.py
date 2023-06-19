# Copyright (c) Microsoft. All rights reserved.

import json

import aiohttp

from semantic_kernel.orchestration.sk_context import SKContext
from semantic_kernel.skill_definition import sk_function, sk_function_context_parameter


class PyseriniSkill:
    """
    A skill that uses Pyserini to search a corpus of documents.

    Usage:
        kernel.import_skill(PyseriniSkill(), "http")

    Examples:

        {{pyserini.search $query}}
    """

    @sk_function(description="Searches a corpus of documents using Pyserini using the specified query.", name="search")
    @sk_function_context_parameter(name="url", description="The url of the request")
    async def search(self, query: str, context: SKContext) -> str:
        """
        Searches a corpus of documents using Pyserini using the specified query.
        Return the response body as a string.

        params:
            query: The query to search for.
            context: The SKContext containing the url of the request.
        returns:
            The response body as a string.
        """
        _, url = context.variables.get("url")
        if not url:
            raise ValueError("url cannot be `None` or empty")

        headers = {"Content-Type": "application/json"}
        body = {"query": query}
        data = json.dumps(body)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url, headers=headers, data=data, raise_for_status=True
            ) as response:
                return await response.text()

