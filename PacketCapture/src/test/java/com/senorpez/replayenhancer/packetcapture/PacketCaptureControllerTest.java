/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.senorpez.replayenhancer.packetcapture;

import javafx.fxml.FXML;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.stage.Stage;
import org.hamcrest.BaseMatcher;
import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.junit.Test;
import org.testfx.api.FxAssert;
import org.testfx.framework.junit.ApplicationTest;

import static org.testfx.matcher.base.NodeMatchers.hasText;
import static org.testfx.matcher.base.NodeMatchers.isDisabled;
import static org.testfx.matcher.base.NodeMatchers.isEnabled;

/**
 *
 * @author senor
 */
public class PacketCaptureControllerTest extends ApplicationTest {
    @FXML
    private Button btnEndCapture;

    @Override
    public void start(Stage stage) throws Exception {
        new PacketCapture().start(stage);
    }

    //    @Override
//    public void start(Stage stage) throws Exception {
//        Parent root = FXMLLoader.load(getClass().getResource("PacketCapture.fxml"));
//        Rectangle2D primaryScreenBounds = Screen.getPrimary().getVisualBounds();
//
//        Scene scene = new Scene(root);
//
//        stage.setScene(scene);
//        stage.setX(primaryScreenBounds.getMinX());
//        stage.setY(primaryScreenBounds.getMinY());
//        stage.show();
//        stage.setMinWidth(stage.getWidth());
//        stage.setMaxWidth(stage.getWidth());
//        stage.setMinHeight(stage.getHeight());
//        stage.setMaxHeight(stage.getHeight());
//        stage.setTitle("Packet Capture");
//    }

    @Test
    public void testButtonStartCaptureText() {
        FxAssert.verifyThat("#btnStartCapture", hasText("Start Capture"));
    }

    @Test
    public void testButtonStartCaptureDisabled() {
        FxAssert.verifyThat("#btnStartCapture", isEnabled());
    }

    @Test
    public void testButtonEndCaptureText() {
        FxAssert.verifyThat("#btnEndCapture", hasText("End Capture"));
    }

    @Test
    public void testButtonEndCaptureDisabled() {
        FxAssert.verifyThat("#btnEndCapture", isDisabled());
    }

    @Test
    public void testTextFieldStorageDirectoryDefaultValue() {
        FxAssert.verifyThat("#txtStorageDirectory", hasText(System.getProperty("user.home")));
    }

    @Test
    public void testButtonSelectStorageDirectoryText() {
        FxAssert.verifyThat("#btnSelectStorageDirectory", hasText("Select..."));
    }

    @Test
    public void testButtonSelectStorageDirectoryEnabled() {
        FxAssert.verifyThat("#btnSelectStorageDirectory", isEnabled());
    }

    private class TextAreaNotEditableMatcher<T> extends BaseMatcher {
        @Override
        public boolean matches(Object o) {
            TextArea textArea = (TextArea) o;
            return !textArea.editableProperty().getValue();
        }

        @Override
        public void describeTo(Description description) {

        }
    }

    @Test
    public void testTextAreaOutputEditable() {
        FxAssert.verifyThat("#txtOutput", (Matcher<Node>) new TextAreaNotEditableMatcher<>());
    }
}