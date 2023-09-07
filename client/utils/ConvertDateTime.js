
export function ConvertDateTime(dateTimeStr){
    return new Date(dateTimeStr).toLocaleString("ru")
}