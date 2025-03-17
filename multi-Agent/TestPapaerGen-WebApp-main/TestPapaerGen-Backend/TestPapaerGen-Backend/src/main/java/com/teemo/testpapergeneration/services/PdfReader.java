package com.teemo.testpapergeneration.services;

import com.alibaba.fastjson.JSONObject;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import java.io.*;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

public class PdfReader {
    private InputStream inputStream;

    public PdfReader(InputStream inputStream) {
        this.inputStream = inputStream;
    }

    public List<JSONObject> readPdf() {
        List<JSONObject> result = new ArrayList<>();
        try (PDDocument document = PDDocument.load(this.inputStream)) {
            PDFTextStripper stripper = new PDFTextStripper();
            String text = stripper.getText(document);
            String[] lines = text.split("\\r?\\n");

            for (String line : lines) {
                JSONObject r = new JSONObject();
                r.put("content", line);
                result.add(r);
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return result;
    }

    public void savePdf(String filepath) throws IOException {
        try (PDDocument document = PDDocument.load(this.inputStream)) {
            File file = new File(filepath);
            try (FileOutputStream outputStream = new FileOutputStream(file)) {
                document.save(outputStream);
            }
        }
    }

    public static void main(String[] args) {
        File file = new File("D:/Desktop/document.pdf");
        try (InputStream inputStream = Files.newInputStream(file.toPath())) {
            PdfReader reader = new PdfReader(inputStream);
            List<JSONObject> result = reader.readPdf();
            System.out.println(result);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
