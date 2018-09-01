# DuReader Dataset

Here is an example of the data:

```
{
    "question_id": 186358,
    "question_type": "YES_NO",
    "question": "上海迪士尼可以带吃的进去吗",
    "documents": [
        {
            "paragraphs": ["text paragraph 1", "text paragraph 2"],
            "title": "上海迪士尼可以带吃的进去吗",
            "bs_rank_pos": 1,
            "is_selected": True
        },
        # ...
    ],
    "answers": [
        "完全密封的可以，其它不可以。",                                        # answer1
        "可以的，不限制的。只要不是易燃易爆的危险物品，一般都可以带进去的。",  # answer2
        "罐装婴儿食品、包装完好的果汁、水等饮料及包装完好的食物都可以带进乐园，但游客自己在家制作的食品是不能入园，因为自制食品有一定的安全隐患。"        # answer3
    ]
    "yesno_answers": [
        "Depends",                      # corresponding to answer 1
        "Yes",                          # corresponding to answer 2
        "Depends"                       # corresponding to asnwer 3
    ]
}
```
"question_id" is the uniq id for each data example.
"question_type" provides 3 question types: "DESCRIPTION", "YES_NO", "ENTITY".
For each 'YES_NO' question,  there is a "yesno_answers" field which contains opinion types ("YES", "NO", "DEPENDS") to corresponding answers. 
For each 'ENTITY' question, there is an 'entity_answers' field containing a list of entity list, and each of the entity list contains named entities extracted from corresponding 'answer' sentences.
For all question types, "documents" field contains at most 5 documents related to the question, and we segment each document into a list of paragraphs and store them in "paragraphs" field. And each web page's title is stored in "title" field.
"is_selected" indicates whether the annotator referred to this document when summarizing the answers. If it is set to False, the annotator didn't choose this document as a reference.
"bs_rank_pos" indicates the rank of this document in Baidu Search, counting from 0.
