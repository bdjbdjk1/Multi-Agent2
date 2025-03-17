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
import java.io.FileWriter;
import java.io.FileReader;
import java.io.BufferedReader;
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
        String scriptPath = currentDirectory + "\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\";
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
    public String generateQuestions(@RequestParam("fileName") String fileName, @RequestParam("questionType") String questionType, @RequestParam("difficulty") String difficulty, @RequestParam("num") String num, @RequestParam("label_1") String label_1, @RequestParam("label_2") String label_2) {
//
        String currentDirectory = new File("").getAbsolutePath();
        String scriptPath = currentDirectory + "\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\input";
//        String scriptPath = "E:\\TestPapaerGen-WebApp-main\\TestPapaerGen-WebApp-main\\TestPapaerGen-Backend\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\app.py";
//        String scriptPath = currentDirectory + "\\add.py";
        pyBuilder pyadd = new pyBuilder();
//        String output = pyadd.runPythonScript("crawler",scriptPath,"5","6");
//        String output = pyadd.runPythonScript("py3.9",scriptPath,fileName,questionType);
        String filepath = currentDirectory + "\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\" + fileName;
        
        String taskid = "taskid.txt"; // 假设taskid是固定的，或者你可以生成一个唯一的taskid
        // 构建文件内容
        String content = " --filename " + fileName + " --type " + questionType + " --difficulty " + difficulty + " --num " + num + " --label_1 " + label_1 + " --label_2 " + label_2;
        // 写入文件
        try (FileWriter writer = new FileWriter(scriptPath + "\\" + taskid)) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
        File file = new File(scriptPath + "\\" + taskid);
        if (file.exists()) {
            file.setReadable(true, false); // 设置其他用户可读
            file.setWritable(true, false); // 设置其他用户可写
        }

        polling = true;
        JSONObject rs = new JSONObject();
        rs.put("polling", polling);
        return myJsonResponse.make200Resp(MyJsonResponse.default_200_response, rs);

    }
    @GetMapping("/getPollStatus")
    public String getPollStatus(){
        String currentDirectory = new File("").getAbsolutePath();
        String scriptPath = currentDirectory + "\\metagpt\\examples\\multiAgentQuestionGenerator\\web\\output";
        File taskFile = new File(scriptPath, "taskid.txt");
        StringBuilder contentBuilder = new StringBuilder();

        // 检查taskid文件是否存在
        if (taskFile.exists()) {
            polling = false; // 文件存在，设置polling为false
            try (FileReader fileReader = new FileReader(taskFile);
                BufferedReader bufferedReader = new BufferedReader(fileReader)) {
                String line;
                while ((line = bufferedReader.readLine()) != null) {
                    contentBuilder.append(line).append("\n");
                }
                output = contentBuilder.toString();
            } catch (IOException e) {
                e.printStackTrace();
            }
            if (!taskFile.delete()) {
                System.out.println("Failed to delete the file: " + taskFile.getName());
            }
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
