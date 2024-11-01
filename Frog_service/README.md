# Frog service

- /frogs/get_all ==> [🐸,🐸,🐸]
- /frogs/get_by_id/{frog_id}/ ==> 🐸 | 404
- /frogs/create/ (FrogSchema) ==> 🐸 | 409
- /frogs/update/ #error ==> "frog updated" | 409
- /frogs/delete/{frog_id}/ ==> "frog deleted"
