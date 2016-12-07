/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.senorpez.replayenhancer.packetcapture;

import java.io.*;
import java.net.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import javafx.fxml.FXML;
import javafx.scene.chart.PieChart;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;

/**
 * FXML Controller class
 *
 * @author senor
 */
public class PacketCaptureController {
    private String timestamp = null;
    private Boolean capture = false;
    private Thread thingThread = null;
    
    @FXML
    private AnchorPane root;
    
    @FXML
    private Button btnStartCapture;
    
    @FXML
    private Button btnEndCapture;
    
    @FXML
    private TextField txtStorageDirectory;
    
    @FXML
    private TextArea txtOutput;
    
    public void initialize() {
        txtStorageDirectory.setText(System.getProperty("user.home"));
        resetAll();
    }
    
    @FXML
    private void selectStorageDirectory() {
        Stage stage = (Stage) root.getScene().getWindow();
        DirectoryChooser directoryChooser = new DirectoryChooser();
        directoryChooser.setTitle("Open Telemetry Storage Directory");
        directoryChooser.setInitialDirectory(
                new File(System.getProperty("user.home")));
        File directory = directoryChooser.showDialog(stage);
        if (directory != null && directory.isDirectory()) {
            try {
                String directoryName = directory.getCanonicalPath();
                txtStorageDirectory.setText(directoryName);
            } catch (IOException e) {
                e.printStackTrace();
            }
        } 
    }
    
    @FXML
    private void resetAll() {
        btnStartCapture.setDisable(false);
        btnStartCapture.setDefaultButton(true);
        btnEndCapture.setDisable(true);
        btnEndCapture.setDefaultButton(false);
        txtOutput.setEditable(false);
        txtOutput.setText("Ready to capture...");
    }
    
    @FXML
    private void startCapture() throws IOException {
        btnStartCapture.setDisable(true);
        btnStartCapture.setDefaultButton(false);
        btnEndCapture.setDisable(false);
        btnEndCapture.setDefaultButton(true);
        txtOutput.setText(txtOutput.getText()+"\nBeginning capture.");
        
        LocalDateTime date = LocalDateTime.now();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss");
        timestamp = date.format(formatter);
        
        File directory = new File(txtStorageDirectory.getText()+File.separator+timestamp);
        boolean success = directory.mkdir();
        if (success) {
            txtOutput.setText(txtOutput.getText()+"\nSaving packets to "+directory.toString());   
            getPacket(timestamp);
        } else {
            txtOutput.setText(txtOutput.getText()+"\nError creating "+directory.toString()+". Packet capture aborted");
            btnEndCapture.setDisable(true);
            btnEndCapture.setDefaultButton(false);
            btnStartCapture.setDisable(false);
            btnStartCapture.setDefaultButton(true);
        }
    }

    @FXML
    private void getPacket(String directory) throws IOException {
        DatagramSocket socket = new DatagramSocket(5606, InetAddress.getByName("0.0.0.0"));

        Runnable captureThread = new Runnable() {
            @Override
            public void run() {
                Integer i = 0;
                while (capture) {
                    byte[] buf = new byte[2048];
                    DatagramPacket packet = new DatagramPacket(buf, buf.length);
                    try {
                        socket.receive(packet);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                    try {
                        FileOutputStream file = new FileOutputStream(txtStorageDirectory.getText() + File.separator + directory + File.separator + "pdata" + i.toString());
                        file.write(buf, 0, packet.getLength());
                        txtOutput.setText(txtOutput.getText()+"\nPacket Size: "+packet.getLength());
                        file.flush();
                        file.close();
                        i += 1;
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        };
        capture = true;
        thingThread = new Thread(captureThread);
        thingThread.start();
    }

    @FXML
    private void endCapture() {
        btnEndCapture.setDisable(true);
        btnEndCapture.setDefaultButton(false);
        btnStartCapture.setDisable(false);
        btnStartCapture.setDefaultButton(true);
        txtOutput.setText(txtOutput.getText()+"\nEnding capture.");

        capture = false;
    }
}
