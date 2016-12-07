package com.senorpez.replayenhancer.configurationeditor;

import javafx.event.Event;
import javafx.scene.control.*;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.util.StringConverter;

/* Adapted from: https://gist.github.com/james-d/be5bbd6255a4640a5357
 */
public class CustomCell<S, T> extends TableCell<S, T> {
    private static final StringConverter<Integer> INTEGER_CONVERTER = new StringConverter<Integer>() {
        @Override
        public String toString(Integer object) {
            return object.toString();
        }

        @Override
        public Integer fromString(String string) {
            return Integer.valueOf(string);
        }
    };
    private static final StringConverter<String> STRING_CONVERTER = new StringConverter<String>() {
        @Override
        public String toString(String object) {
            return object;
        }

        @Override
        public String fromString(String string) {
            return string;
        }
    };
    private final TextField textField = new TextField();
    private final StringConverter<T> converter;

    private CustomCell(StringConverter<T> converter) {
        this.converter = converter;

        itemProperty().addListener((observable, oldValue, newValue) -> {
            if (newValue == null) {
                setText(null);
            } else {
                setText(converter.toString(newValue));
            }
        });
        setGraphic(textField);
        setContentDisplay(ContentDisplay.TEXT_ONLY);

        textField.setOnAction(event -> commitEdit(converter.fromString(textField.getText())));
        textField.focusedProperty().addListener((observable, oldValue, newValue) -> {
            if (!newValue) {
                commitEdit(converter.fromString(textField.getText()));
            }
        });
        textField.addEventFilter(KeyEvent.KEY_PRESSED, event -> {
            if (event.getCode() == KeyCode.ESCAPE) {
                textField.setText(converter.toString(getItem()));
                cancelEdit();
                event.consume();
            }
        });
    }

    public static <S> CustomCell<S, Integer> createIntegerEditCell() {
        return new CustomCell<>(INTEGER_CONVERTER);
    }

    public static <S> CustomCell<S, String> createStringEditCell() {
        return new CustomCell<>(STRING_CONVERTER);
    }

    @Override
    public void startEdit() {
        super.startEdit();
        textField.setText(converter.toString(getItem()));
        setContentDisplay(ContentDisplay.GRAPHIC_ONLY);
        textField.requestFocus();
    }

    @Override
    public void commitEdit(T newValue) {
        if (!isEditing() && !newValue.equals(getItem())) {
            TableView<S> table = getTableView();
            if (table != null) {
                TableColumn<S, T> column = getTableColumn();
                TableColumn.CellEditEvent<S, T> event = new TableColumn.CellEditEvent<>(table,
                        new TablePosition<>(table, getIndex(), column),
                        TableColumn.editCommitEvent(), newValue);
                Event.fireEvent(column, event);
                /* TODO: 10/27/2016 Figure out why we need a refresh here. */
                table.refresh();
            }
        }
        super.commitEdit(newValue);
        setContentDisplay(ContentDisplay.TEXT_ONLY);
    }

    @Override
    public void cancelEdit() {
        super.cancelEdit();
        setContentDisplay(ContentDisplay.TEXT_ONLY);
    }
}
