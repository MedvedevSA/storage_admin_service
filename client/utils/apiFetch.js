
export async function apiFetch(route, options = {}){
    if (['PUT', 'POST'].includes(options.method)){
        options.headers ={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }
    return fetch('http://localhost:8000' + route ,options)
}