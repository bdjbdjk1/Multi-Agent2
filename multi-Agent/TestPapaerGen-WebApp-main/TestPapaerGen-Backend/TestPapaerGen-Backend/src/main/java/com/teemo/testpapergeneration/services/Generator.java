package com.teemo.testpapergeneration.services;

import com.alibaba.fastjson.JSONObject;

import java.util.List;

public class Generator {
    public String generatePaper(List<JSONObject> data, String questionType) {
        StringBuilder paper = new StringBuilder();
        paper.append("题目类型: ").append(questionType).append("\n\n");

        for (JSONObject item : data) {
            paper.append("题目内容: ").append(item.getString("content")).append("\n");
        }
        return paper.toString();
    }

    public static void main(String[] args) {
        // 模拟数据
        List<JSONObject> data = List.of(
                new JSONObject().fluentPut("content", "题目1: 这是一个选择题"),
                new JSONObject().fluentPut("content", "题目2: 这是一个填空题"),
                new JSONObject().fluentPut("content", "题目3: 这是一个简答题")
        );

        Generator generator = new Generator();
        String paper = generator.generatePaper(data, "选择题");
        System.out.println(paper);
    }
}
