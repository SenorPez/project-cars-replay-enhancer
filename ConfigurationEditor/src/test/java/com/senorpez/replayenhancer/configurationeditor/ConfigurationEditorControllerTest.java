/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.senorpez.replayenhancer.configurationeditor;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.collections.ObservableList;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import static org.junit.Assert.*;

/**
 *
 * @author SenorPez
 */
public class ConfigurationEditorControllerTest {
    
    public ConfigurationEditorControllerTest() {
    }

    @BeforeClass
    public static void setUpClass() throws Exception {
    }

    @AfterClass
    public static void tearDownClass() throws Exception {
    }

    @Before
    public void setUp() throws Exception {
    }

    @After
    public void tearDown() throws Exception {
    }

    /**
     * Test of initialize method, of class ConfigurationEditorController.
     */
    @Test
    public void testTrue() {
        System.out.println("True");
        assertTrue("True is False", true);
    }
    
    @Test
    public void testFalse() {
        System.out.println("False");
        assertFalse("False is False", false);
    }
    

}
