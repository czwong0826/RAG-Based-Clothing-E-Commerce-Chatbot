import json

d = {
    "name":"Ali",
    "age":11,
    "gender":"male"
} 

s = json.dumps(d, ensure_ascii=False)
print(s)



l = [
    {
    "name":"Ali",
    "age":11,
    "gender":"male"
    },
    {
    "name":"Bryan",
    "age":12,
    "gender":"male"
    }
]

print(json.dumps(l, ensure_ascii=False))



json_str = '{"name": "Ali", "age": 11, "gender": "male"}'
json_arr_str = '[{"name": "Ali", "age": 11, "gender": "male"}, {"name": "Bryan", "age": 12, "gender": "male"}]'

res_dict = json.loads(json_str)
print(res_dict,type(res_dict))

res_list = json.loads(json_arr_str)
print(res_list,type(res_list))
