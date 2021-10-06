function asyncRequest(value, requestPath)
{
    return fetch(`${window.origin}/` + requestPath,
        {
            method: "POST",
            credentials: "include",
            body: JSON.stringify(value),
            cache: "no-cache",
            headers: new Headers({ "content-type": "application/json" })
        })
}