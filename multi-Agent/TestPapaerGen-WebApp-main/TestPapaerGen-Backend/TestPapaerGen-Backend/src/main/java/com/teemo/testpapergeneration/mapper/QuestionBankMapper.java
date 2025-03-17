package com.teemo.testpapergeneration.mapper;

import com.teemo.testpapergeneration.entity.QuestionBank;
import org.apache.ibatis.annotations.*;

import java.util.List;

@Mapper
public interface QuestionBankMapper {

    @Select("select * from QuestionBank order by update_time desc")
    public List<QuestionBank> getAllQuestionBank();

    @Select("SELECT DISTINCT topic_type FROM QuestionBank")
    public List<String> getDistinctTopicType();

    public List<QuestionBank> searchQuestionByTopic(String topicType, String keyword);

    @Insert("insert into QuestionBank" +
            "(topic, topic_material_id, answer, topic_type, score, " +
            "difficulty, chapter_1, chapter_2, label_1, label_2," +
            "update_time) values(#{topic}, #{topic_material_id}, #{answer}, #{topic_type}, " +
            "#{score}, #{difficulty}, #{chapter_1}, #{chapter_2}, " +
            "#{label_1}, #{label_2}, #{update_time})")
    public Integer insertSingleQuestionBank(QuestionBank questionBank);

    @Delete("delete from QuestionBank where id=#{id}")
    public Integer deleteSingleQuestionBank(Integer id);

    @Select("select * from QuestionBank where id=#{id}")
    public List<QuestionBank> getQuestionBankById(Integer id);

    @Update("update QuestionBank set " +
            "topic=#{topic}, topic_material_id=#{topic_material_id}, answer=#{answer}, topic_type=#{topic_type}, " +
            "score=#{score}, difficulty=#{difficulty}, chapter_1=#{chapter_1}, chapter_2=#{chapter_2}, " +
            "label_1=#{label_1}, label_2=#{label_2}, update_time=#{update_time} where id=#{id}")
    public Integer updateSingleQuestionBank(QuestionBank questionBank);

    // 根据题目的ids查询题目的难度
    public Double getAvgDifficultyByIds(@Param("ids") List<Integer> ids);

    // 根据ids查询不在ids列表里的题目
    public List<QuestionBank> getQuestionBankByIds(@Param("ids") List<Integer> ids,
                                                   @Param("generateRange") List<String> generateRange);

    // test
    public List<QuestionBank> getAll();

    // 概览页统计

    // 获取题库表的Label2
    @Select("select distinct label_1 from QuestionBank")
    public List<String> getDistinctLabel2FromQuestionBank();

    // 根据Label2查询数量
    @Select("select count(*) from QuestionBank where label_2=#{label_2}")
    public Integer getQuestionBankCountByLabel2(String label_2);

    // 获取题库表的score
    @Select("select distinct score from QuestionBank")
    public List<Double> getDistinctScoreFromQuestionBank();

    // 根据Label2查询数量
    @Select("select count(*) from QuestionBank where score=#{score}")
    public Integer getQuestionBankCountByScore(Double score);

}
