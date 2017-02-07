# DataServer
Small service writen on python

Rules to generate JSON http://www.json-generator.com/

```
[
  '{{repeat(5, 7)}}',
  {
    object_id: '{{objectId()}}',
    object_type: '{{random("generate", "eat", "redirect")}}',
    table_model: '{{objectId()}}',
    name: '{{company().toUpperCase()}}',
    description: '{{lorem(1, "paragraphs")}}',
    isActive: '{{bool()}}',
    options: [
      '{{repeat(3)}}',
      {
        id: '{{index()}}',
        option_type: '{{lorem(1, "words")}}',
        value: '{{floating(0, 1)}}',
        status: '{{bool()}}'
      }
    ]
  }
]
```
