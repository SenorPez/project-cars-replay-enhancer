package com.senorpez.replayenhancer.configurationeditor;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.geometry.Rectangle2D;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Screen;
import javafx.stage.Stage;

import java.io.IOException;
import java.util.logging.ConsoleHandler;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ConfigurationEditor extends Application {
    private static final Logger LOGGER;

    static {
        Logger tmp = Logger.getLogger("com.senorpez.replayenhancer");
        try {
            tmp.addHandler(new FileHandler("replayenhancer.log"));
        } catch (IOException e) {
            tmp.addHandler(new ConsoleHandler());
        }
        LOGGER = tmp;
    }

    public static void main(String[] args) {
        Thread.setDefaultUncaughtExceptionHandler((t, e) -> {
            LOGGER.log(Level.SEVERE, "Exception in thread: " + t, e);
            System.exit(1);
        });
        launch(args);
    }

    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("ConfigurationEditor.fxml"));
        Rectangle2D primaryScreenBounds = Screen.getPrimary().getVisualBounds();

        Scene scene = new Scene(root);

        stage.setScene(scene);
        stage.setX(primaryScreenBounds.getMinX());
        stage.setY(primaryScreenBounds.getMinY());
        stage.show();
        stage.setMinWidth(stage.getWidth());
        stage.setMaxWidth(stage.getWidth());
        stage.setMaxHeight(stage.getHeight());

        if (stage.getHeight() > primaryScreenBounds.getHeight()) {
            stage.setHeight(primaryScreenBounds.getHeight()*.90);
        }

        stage.setTitle("Project CARS Replay Enhancer Configuration Editor");
    }
    
}
