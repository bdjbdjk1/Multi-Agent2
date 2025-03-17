package com.teemo.testpapergeneration.controller;
import com.teemo.testpapergeneration.services.PdfReader;
import com.teemo.testpapergeneration.services.Generator;
import com.alibaba.fastjson.JSONObject;
import com.teemo.testpapergeneration.entity.QuestionBank;
import com.teemo.testpapergeneration.mapper.QuestionBankMapper;
import com.teemo.testpapergeneration.services.ExcelReader;
import com.teemo.testpapergeneration.services.pyBuilder;
import com.teemo.testpapergeneration.utils.MyJsonResponse;
import org.apache.poi.openxml4j.exceptions.InvalidFormatException;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

@RestController
public class AgentController {
    private final ExecutorService executorService = Executors.newSingleThreadExecutor();
    private Future<String> outputFuture;
    MyJsonResponse myJsonResponse = new MyJsonResponse();
    String output = null;
    boolean polling = false;

    @PostMapping("/uploadPdf")
    public String uploadPdf(@RequestParam("file") MultipartFile file) {

        // 转换成输入流
        InputStream inputStream;
        try {
            inputStream = file.getInputStream();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        String originalFileName = file.getOriginalFilename();
        PdfReader pr = new PdfReader(inputStream);
        String currentDirectory = new File("").getAbsolutePath();
        String scriptPath = currentDirectory + "\\target\\classes\\static\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\";
        String filepath = scriptPath + originalFileName;
        try {
            pr.savePdf(filepath); // 确保提供文件名和扩展名
        } catch (IOException e) {
            // 这里可以处理异常，例如打印错误信息
            System.err.println("An error occurred while saving the PDF file: " + e.getMessage());
        }
        JSONObject rs = new JSONObject();
        rs.put("filename", originalFileName);
        return myJsonResponse.make200Resp(MyJsonResponse.default_200_response, rs);
    }

    @PostMapping("/generateQuestions")
    public String uploadPdf(@RequestParam("fileName") String fileName, @RequestParam("questionType") String questionType, @RequestParam("difficulty") String difficulty, @RequestParam("num") String num, @RequestParam("label_1") String label_1, @RequestParam("label_2") String label_2) {
//
        String currentDirectory = new File("").getAbsolutePath();
        String scriptPath = currentDirectory + "\\target\\classes\\static\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\app.py";
//        String scriptPath = "E:\\TestPapaerGen-WebApp-main\\TestPapaerGen-WebApp-main\\TestPapaerGen-Backend\\target\\classes\\static\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\app.py";
//        String scriptPath = currentDirectory + "\\target\\classes\\static\\add.py";
        pyBuilder pyadd = new pyBuilder();
//        String output = pyadd.runPythonScript("crawler",scriptPath,"5","6");
//        String output = pyadd.runPythonScript("py3.9",scriptPath,fileName,questionType);
        String filepath = currentDirectory + "\\target\\classes\\static\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\" + fileName;
        outputFuture = executorService.submit(() -> {
//            String result = pyadd.runPythonScript("crawler", scriptPath, "5", "6");
            return pyadd.runPythonScript("Meta", scriptPath, filepath, questionType, difficulty, num, label_1, label_2);
//            System.out.println("outputfuture:"+result);
//            return result;
        });

        polling = true;
        JSONObject rs = new JSONObject();
        rs.put("polling", polling);
        return myJsonResponse.make200Resp(MyJsonResponse.default_200_response, rs);

    }
    @GetMapping("/getPollStatus")
    public String getPollStatus(){
        try {
            if (outputFuture.isDone()) {
                output = outputFuture.get();
                polling = false;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        JSONObject rs = new JSONObject();
        rs.put("polling", polling);
        return myJsonResponse.make200Resp(MyJsonResponse.default_200_response, rs);
    }
    @GetMapping(value = "/getQuestions", produces = "text/plain;charset=UTF-8")
    public String getQuestions(){
        JSONObject rs = new JSONObject();
        rs.put("questions", output);
        // rs.put("questions", "测试成功");
//        ArrayList<JSONObject> ret = new ArrayList<>();
//        JSONObject _tmp = new JSONObject();
//        _tmp.put("questions", "题目生成成功：");
//        ret.add(_tmp);
//        JSONObject _tmp1 = new JSONObject();
//        _tmp1.put("questions", output);
//        ret.add(_tmp1);
        return myJsonResponse.make200Resp(MyJsonResponse.default_200_response, rs);
    }
}
