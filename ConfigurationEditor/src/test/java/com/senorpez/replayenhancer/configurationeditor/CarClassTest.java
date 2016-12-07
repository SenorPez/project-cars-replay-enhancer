package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.scene.paint.Color;
import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.junit.Assert.*;

public class CarClassTest {
    private static final String carClassName = "Vintage F1 C";
    private static final Color carClassColor = Color.rgb(255, 0, 0);
    private static CarClass instance;

    @Before
    public void setUp() throws Exception {
        instance = new CarClass(carClassName, carClassColor);
    }

    @Test
    public void getClassName() throws Exception {
        String expResult = carClassName;
        String result = instance.getClassName();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setClassName() throws Exception {
        instance.setClassName("New Class Name");
    }

    @Test
    public void classNameProperty() throws Exception {
        SimpleStringProperty expResult = new SimpleStringProperty();
        SimpleStringProperty result = instance.classNameProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getClassColor() throws Exception {
        Color expResult = carClassColor;
        Color result = instance.getClassColor();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setClassColor() throws Exception {
        instance.setClassColor(Color.rgb(0, 255, 0));
    }

    @Test
    public void classColorProperty() throws Exception {
        SimpleObjectProperty<Color> expResult = new SimpleObjectProperty<>();
        SimpleObjectProperty<Color> result = instance.classColorProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }
}
