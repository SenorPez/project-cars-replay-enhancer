package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import org.junit.Before;
import org.junit.Test;

import static org.hamcrest.CoreMatchers.instanceOf;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.hamcrest.core.IsEqual.equalTo;
import static org.mockito.Mockito.mock;


public class CarTest {
    private static final String carName = "Lotus 98T";
    private static Car instance;

    @Before
    public void setUp() throws Exception {
        instance = new Car(carName, mock(CarClass.class));
    }

    @Test
    public void getCarName() throws Exception {
        String expResult = carName;
        String result = instance.getCarName();
        assertThat(result, equalTo(expResult));
    }

    @Test
    public void setCarName() throws Exception {
        instance.setCarName("New Car");
    }

    @Test
    public void carNameProperty() throws Exception {
        SimpleStringProperty expResult = new SimpleStringProperty();
        SimpleStringProperty result = instance.carNameProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void getCarClass() throws Exception {
        CarClass expResult = mock(CarClass.class);
        CarClass result = instance.getCarClass();
        assertThat(result, instanceOf(expResult.getClass()));
    }

    @Test
    public void setCarClass() throws Exception {
        instance.setCarClass(mock(CarClass.class));
    }

    @Test
    public void carClassProperty() throws Exception {
        SimpleObjectProperty<CarClass> expResult = new SimpleObjectProperty<>();
        SimpleObjectProperty<CarClass> result = instance.carClassProperty();
        assertThat(result, instanceOf(expResult.getClass()));
    }
}
