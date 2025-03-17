package com.teemo.testpapergeneration.services;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Objects;

import java.nio.charset.Charset;

public class pyBuilder {

    public String runPythonScript(String anacondaEnv, String scriptPath, String filename, String type,String difficulty,String num,String label_1,String label_2) {
        
        Charset defaultCharset = Charset.defaultCharset();
        System.out.println("System default charset: " + defaultCharset.name());
        
        String command = "cmd /c \"activate " + anacondaEnv + " && python " + scriptPath + " --filename " + filename + " --type " + type + " --difficulty " + difficulty + " --num " + num + " --label_1 " + label_1 + " --label_2 " + label_2 + "\"";
        System.err.println("command:"+ command);
        // 用于捕获输出的字符串构建器
        StringBuilder output = new StringBuilder();

        try {
            // 启动进程
//            Process process = processBuilder.start();
            Process process = Runtime.getRuntime().exec(command);
            // 读取输出流
            // BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream(),"UTF-8"));
            // String line;
            // while ((line = reader.readLine()) != null) {
            //     System.out.println(line);
            //     output.append(line).append("\n");
            // }

            // 等待进程结束
            int exitCode = process.waitFor();
            if (exitCode == 0) {
                // 进程正常结束
                return output.toString();
            } else {
                // 处理错误情况
                return "Python script exited with error code: " + exitCode;
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return "An exception occurred while running the Python script: " + e.getMessage();
        }
    }
}