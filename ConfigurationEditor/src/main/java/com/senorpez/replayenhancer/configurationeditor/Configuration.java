package com.senorpez.replayenhancer.configurationeditor;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;
import javafx.beans.Observable;
import javafx.beans.property.*;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.scene.paint.Color;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@JsonPropertyOrder(alphabetic = true)
// TODO: 10/20/2016 Add functionality for deprecation of old, used properties. For now, here.
@JsonIgnoreProperties(value = {"video_cache", "video_gaptime", "video_threshold"})
public class Configuration {
    // Source Data
    @JsonProperty(value = "source_video")
    private final SimpleObjectProperty<File> sourceVideo;

    @JsonProperty(value = "source_telemetry")
    private final SimpleObjectProperty<File> sourceTelemetry;

    // Source Parameters
    @JsonProperty(value = "video_skipstart")
    private final SimpleDoubleProperty videoStartTime;

    @JsonProperty(value = "video_skipend")
    private final SimpleDoubleProperty videoEndTime;

    @JsonProperty(value = "sync_racestart")
    private final SimpleDoubleProperty syncRacestart;

    // Output
    @JsonProperty(value = "output_video")
    private final SimpleObjectProperty<File> outputVideo;

    //Headings
    @JsonProperty(value = "heading_text")
    private final SimpleStringProperty headingText;

    @JsonProperty(value = "subheading_text")
    private final SimpleStringProperty subheadingText;

    @JsonProperty(value = "heading_font")
    private final SimpleObjectProperty<File> headingFont;

    @JsonProperty(value = "heading_font_size")
    private final SimpleIntegerProperty headingFontSize;

    @JsonDeserialize(using = Configuration.ColorDeserializer.class)
    @JsonProperty(value = "heading_font_color")
    @JsonSerialize(using = Configuration.ColorSerializer.class)
    private final SimpleObjectProperty<Color> headingFontColor;

    @JsonDeserialize(using = Configuration.ColorDeserializer.class)
    @JsonProperty(value = "heading_color")
    @JsonSerialize(using = Configuration.ColorSerializer.class)
    private final SimpleObjectProperty<Color> headingColor;

    @JsonProperty(value = "series_logo")
    private final SimpleObjectProperty<File> seriesLogo;

    // Backgrounds
    @JsonProperty(value = "backdrop")
    private final SimpleObjectProperty<File> backdrop;

    @JsonProperty(value = "logo")
    private final SimpleObjectProperty<File> logo;

    @JsonProperty(value = "logo_height")
    private final SimpleIntegerProperty logoHeight;

    @JsonProperty(value = "logo_width")
    private final SimpleIntegerProperty logoWidth;

    // Font
    @JsonProperty(value = "font")
    private final SimpleObjectProperty<File> font;

    @JsonProperty(value = "font_size")
    private final SimpleIntegerProperty fontSize;

    @JsonDeserialize(using = Configuration.ColorDeserializer.class)
    @JsonProperty(value = "font_color")
    @JsonSerialize(using = Configuration.ColorSerializer.class)
    private final SimpleObjectProperty<Color> fontColor;

    // Layout
    @JsonProperty(value = "margin")
    private final SimpleIntegerProperty margin;

    @JsonProperty(value = "column_margin")
    private final SimpleIntegerProperty columnMargin;

    @JsonProperty(value = "result_lines")
    private final SimpleIntegerProperty resultLines;

    @JsonProperty(value = "leader_window_size")
    private final SimpleIntegerProperty leaderStandingsLines;

    @JsonProperty(value = "field_window_size")
    private final SimpleIntegerProperty windowStandingsLines;

    // Options
    @JsonProperty(value = "show_champion")
    private final SimpleBooleanProperty showChampion;

    @JsonProperty(value = "hide_series_zeros")
    private final SimpleBooleanProperty hideSeriesZeros;

    @JsonDeserialize(using = Configuration.PointStructureDeserializer.class)
    @JsonProperty(value = "point_structure")
    @JsonSerialize(using = Configuration.PointStructureSerializer.class)
    private final SimpleListProperty<PointStructureItem> pointStructure;

    @JsonDeserialize(using = Configuration.ParticipantConfigurationDeserializer.class)
    @JsonProperty(value = "participant_config")
    @JsonSerialize(using = Configuration.ParticipantConfigurationSerializer.class)
    private final SimpleListProperty<Driver> participantConfiguration;

    @JsonDeserialize(using = Configuration.ParticipantConfigurationDeserializer.class)
    @JsonProperty(value = "additional_participant_config")
    @JsonSerialize(using = Configuration.ParticipantConfigurationSerializer.class)
    private final SimpleListProperty<Driver> additionalParticipantConfiguration;

    @JsonIgnore
    private final SimpleListProperty<Car> cars;

    public Configuration() {
        // Source Data
        this.sourceVideo = new SimpleObjectProperty<>();
        this.sourceTelemetry = new SimpleObjectProperty<>();

        // Source Parameters
        this.videoStartTime = new SimpleDoubleProperty(0.0);
        this.videoEndTime = new SimpleDoubleProperty(0.0);
        this.syncRacestart = new SimpleDoubleProperty(0.0);

        // Output
        this.outputVideo = new SimpleObjectProperty<>();

        // Headings
        this.headingText = new SimpleStringProperty();
        this.subheadingText = new SimpleStringProperty();
        this.headingFont = new SimpleObjectProperty<>();
        this.headingFontSize = new SimpleIntegerProperty(20);
        this.headingFontColor = new SimpleObjectProperty<>(Color.rgb(255, 255, 255));
        this.headingColor = new SimpleObjectProperty<>(Color.rgb(255, 0, 0));
        this.seriesLogo = new SimpleObjectProperty<>();

        // Backgrounds
        this.backdrop = new SimpleObjectProperty<>();
        this.logo = new SimpleObjectProperty<>();
        this.logoHeight = new SimpleIntegerProperty(150);
        this.logoWidth = new SimpleIntegerProperty(150);

        // Font
        this.font = new SimpleObjectProperty<>();
        this.fontSize = new SimpleIntegerProperty(15);
        this.fontColor = new SimpleObjectProperty<>(Color.rgb(0, 0, 0));

        // Layout
        this.margin = new SimpleIntegerProperty(20);
        this.columnMargin = new SimpleIntegerProperty(10);
        this.resultLines = new SimpleIntegerProperty(10);
        this.leaderStandingsLines = new SimpleIntegerProperty(10);
        this.windowStandingsLines = new SimpleIntegerProperty(0);

        // Options
        this.showChampion = new SimpleBooleanProperty(false);
        this.hideSeriesZeros = new SimpleBooleanProperty(false);

        List<Integer> defaultPoints = new ArrayList<>(Arrays.asList(5, 25, 18, 15, 12, 10, 8, 6, 4, 2, 1));
        ObservableList<PointStructureItem> defaultPointStructure = FXCollections.observableArrayList();
        Integer index = 0;
        for (Integer points : defaultPoints) {
            defaultPointStructure.add(new PointStructureItem(index, points));
            index += 1;
        }
        this.pointStructure = new SimpleListProperty<>(defaultPointStructure);

        this.participantConfiguration = new SimpleListProperty<>(FXCollections.observableList(new ArrayList<Driver>(), param -> new Observable[]{param.getCar().carNameProperty()}));
        this.additionalParticipantConfiguration = new SimpleListProperty<>(FXCollections.observableList(new ArrayList<Driver>(), param -> new Observable[]{param.getCar().carNameProperty()}));

        this.cars = new SimpleListProperty<>(FXCollections.observableArrayList(new TreeSet<>()));

        this.participantConfiguration.addListener(((observable, oldValue, newValue) -> cars.set(FXCollections.observableArrayList(Stream.concat(
                newValue.stream().map(Driver::getCar), additionalParticipantConfiguration.stream().map(Driver::getCar))
                .collect(Collectors.toCollection(
                        () -> new TreeSet<>(
                                (o1, o2) -> o1.getCarName().compareTo(o2.getCarName())
                        )
                ))
        ))));
        this.additionalParticipantConfiguration.addListener(((observable, oldValue, newValue) -> cars.set(FXCollections.observableArrayList(Stream.concat(
                newValue.stream().map(Driver::getCar), participantConfiguration.stream().map(Driver::getCar))
                .collect(Collectors.toCollection(
                        () -> new TreeSet<>(
                                (o1, o2) -> o1.getCarName().compareTo(o2.getCarName())
                        )
                ))
        ))));
    }

    public File getSourceVideo() {
        return sourceVideo.get();
    }

    public void setSourceVideo(File sourceVideo) {
        this.sourceVideo.set(sourceVideo);
    }

    public SimpleObjectProperty<File> sourceVideoProperty() {
        return sourceVideo;
    }

    public File getSourceTelemetry() {
        return sourceTelemetry.get();
    }

    public void setSourceTelemetry(File sourceTelemetry) {
        this.sourceTelemetry.set(sourceTelemetry);
    }

    public SimpleObjectProperty<File> sourceTelemetryProperty() {
        return sourceTelemetry;
    }

    public double getVideoStartTime() {
        return videoStartTime.get();
    }

    public void setVideoStartTime(double videoStartTime) {
        this.videoStartTime.set(videoStartTime);
    }

    public SimpleDoubleProperty videoStartTimeProperty() {
        return videoStartTime;
    }

    public double getVideoEndTime() {
        return videoEndTime.get();
    }

    public void setVideoEndTime(double videoEndTime) {
        this.videoEndTime.set(videoEndTime);
    }

    public SimpleDoubleProperty videoEndTimeProperty() {
        return videoEndTime;
    }

    public double getSyncRacestart() {
        return syncRacestart.get();
    }

    public void setSyncRacestart(double syncRacestart) {
        this.syncRacestart.set(syncRacestart);
    }

    public SimpleDoubleProperty syncRacestartProperty() {
        return syncRacestart;
    }

    public File getOutputVideo() {
        return outputVideo.get();
    }

    public void setOutputVideo(File outputVideo) {
        this.outputVideo.set(outputVideo);
    }

    public SimpleObjectProperty<File> outputVideoProperty() {
        return outputVideo;
    }

    public String getHeadingText() {
        return headingText.get();
    }

    public void setHeadingText(String headingText) {
        this.headingText.set(headingText);
    }

    public SimpleStringProperty headingTextProperty() {
        return headingText;
    }

    public String getSubheadingText() {
        return subheadingText.get();
    }

    public void setSubheadingText(String subheadingText) {
        this.subheadingText.set(subheadingText);
    }

    public SimpleStringProperty subheadingTextProperty() {
        return subheadingText;
    }

    public File getHeadingFont() {
        return headingFont.get();
    }

    public void setHeadingFont(File headingFont) {
        this.headingFont.set(headingFont);
    }

    public SimpleObjectProperty<File> headingFontProperty() {
        return headingFont;
    }

    public int getHeadingFontSize() {
        return headingFontSize.get();
    }

    public void setHeadingFontSize(int headingFontSize) {
        this.headingFontSize.set(headingFontSize);
    }

    public SimpleIntegerProperty headingFontSizeProperty() {
        return headingFontSize;
    }

    public Color getHeadingFontColor() {
        return headingFontColor.get();
    }

    public void setHeadingFontColor(Color headingFontColor) {
        this.headingFontColor.set(headingFontColor);
    }

    public SimpleObjectProperty<Color> headingFontColorProperty() {
        return headingFontColor;
    }

    public Color getHeadingColor() {
        return headingColor.get();
    }

    public void setHeadingColor(Color headingColor) {
        this.headingColor.set(headingColor);
    }

    public SimpleObjectProperty<Color> headingColorProperty() {
        return headingColor;
    }

    public File getSeriesLogo() {
        return seriesLogo.get();
    }

    public void setSeriesLogo(File seriesLogo) {
        this.seriesLogo.set(seriesLogo);
    }

    public SimpleObjectProperty<File> seriesLogoProperty() {
        return seriesLogo;
    }

    public File getBackdrop() {
        return backdrop.get();
    }

    public void setBackdrop(File backdrop) {
        this.backdrop.set(backdrop);
    }

    public SimpleObjectProperty<File> backdropProperty() {
        return backdrop;
    }

    public File getLogo() {
        return logo.get();
    }

    public void setLogo(File logo) {
        this.logo.set(logo);
    }

    public SimpleObjectProperty<File> logoProperty() {
        return logo;
    }

    public int getLogoHeight() {
        return logoHeight.get();
    }

    public void setLogoHeight(int logoHeight) {
        this.logoHeight.set(logoHeight);
    }

    public SimpleIntegerProperty logoHeightProperty() {
        return logoHeight;
    }

    public int getLogoWidth() {
        return logoWidth.get();
    }

    public void setLogoWidth(int logoWidth) {
        this.logoWidth.set(logoWidth);
    }

    public SimpleIntegerProperty logoWidthProperty() {
        return logoWidth;
    }

    public File getFont() {
        return font.get();
    }

    public void setFont(File font) {
        this.font.set(font);
    }

    public SimpleObjectProperty<File> fontProperty() {
        return font;
    }

    public int getFontSize() {
        return fontSize.get();
    }

    public void setFontSize(int fontSize) {
        this.fontSize.set(fontSize);
    }

    public SimpleIntegerProperty fontSizeProperty() {
        return fontSize;
    }

    public Color getFontColor() {
        return fontColor.get();
    }

    public void setFontColor(Color fontColor) {
        this.fontColor.set(fontColor);
    }

    public SimpleObjectProperty<Color> fontColorProperty() {
        return fontColor;
    }

    public int getMargin() {
        return margin.get();
    }

    public void setMargin(int margin) {
        this.margin.set(margin);
    }

    public SimpleIntegerProperty marginProperty() {
        return margin;
    }

    public int getColumnMargin() {
        return columnMargin.get();
    }

    public void setColumnMargin(int columnMargin) {
        this.columnMargin.set(columnMargin);
    }

    public SimpleIntegerProperty columnMarginProperty() {
        return columnMargin;
    }

    public int getResultLines() {
        return resultLines.get();
    }

    public void setResultLines(int resultLines) {
        this.resultLines.set(resultLines);
    }

    public SimpleIntegerProperty resultLinesProperty() {
        return resultLines;
    }

    public int getLeaderStandingsLines() {
        return leaderStandingsLines.get();
    }

    public SimpleIntegerProperty leaderStandingsLinesProperty() {
        return leaderStandingsLines;
    }

    public void setLeaderStandingsLines(int leaderStandingsLines) {
        this.leaderStandingsLines.set(leaderStandingsLines);
    }

    public int getWindowStandingsLines() {
        return windowStandingsLines.get();
    }

    public SimpleIntegerProperty windowStandingsLinesProperty() {
        return windowStandingsLines;
    }

    public void setWindowStandingsLines(int windowStandingsLines) {
        this.windowStandingsLines.set(windowStandingsLines);
    }

    public boolean isShowChampion() {
        return showChampion.get();
    }

    public void setShowChampion(boolean showChampion) {
        this.showChampion.set(showChampion);
    }

    public SimpleBooleanProperty showChampionProperty() {
        return showChampion;
    }

    public boolean isHideSeriesZeros() {
        return hideSeriesZeros.get();
    }

    public SimpleBooleanProperty hideSeriesZerosProperty() {
        return hideSeriesZeros;
    }

    public void setHideSeriesZeros(boolean hideSeriesZeros) {
        this.hideSeriesZeros.set(hideSeriesZeros);
    }

    public ObservableList<PointStructureItem> getPointStructure() {
        return pointStructure.get();
    }

    public void setPointStructure(ObservableList<PointStructureItem> pointStructure) {
        this.pointStructure.set(pointStructure);
    }

    public SimpleListProperty<PointStructureItem> pointStructureProperty() {
        return pointStructure;
    }

    public ObservableList<Driver> getParticipantConfiguration() {
        return participantConfiguration.get();
    }

    public void setParticipantConfiguration(ObservableList<Driver> participantConfiguration) {
        this.participantConfiguration.set(participantConfiguration);
    }

    public SimpleListProperty<Driver> participantConfigurationProperty() {
        return participantConfiguration;
    }

    public ObservableList<Driver> getAdditionalParticipantConfiguration() {
        return additionalParticipantConfiguration.get();
    }

    public SimpleListProperty<Driver> additionalParticipantConfigurationProperty() {
        return additionalParticipantConfiguration;
    }

    public void setAdditionalParticipantConfiguration(ObservableList<Driver> additionalParticipantConfiguration) {
        this.additionalParticipantConfiguration.set(additionalParticipantConfiguration);
    }

    public ObservableList<Car> getCars() {
        return cars.get();
    }

    public void setCars(ObservableList<Car> cars) {
        this.cars.set(cars);
    }

    public SimpleListProperty<Car> carsProperty() {
        return cars;
    }

    private static class ColorDeserializer extends StdDeserializer<Color> {
        public ColorDeserializer() {
            this(null);
        }

        public ColorDeserializer(Class<?> vc) {
            super(vc);
        }

        @Override
        public Color deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
            JsonNode node = p.getCodec().readTree(p);
            ArrayList<Integer> color_values = new ArrayList<>();
            for (final JsonNode entry : node) {
                color_values.add(entry.asInt());
            }
            return Color.rgb(color_values.get(0), color_values.get(1), color_values.get(2));
        }
    }

    private static class ColorSerializer extends StdSerializer<Color> {
        public ColorSerializer() {
            this(null);
        }

        public ColorSerializer(Class<Color> t) {
            super(t);
        }

        @Override
        public void serialize(Color value, JsonGenerator gen, SerializerProvider provider) throws IOException {
            int[] color_values = new int[3];
            color_values[0] = (int) (value.getRed() * 255);
            color_values[1] = (int) (value.getGreen() * 255);
            color_values[2] = (int) (value.getBlue() * 255);
            gen.writeArray(color_values, 0, 3);
        }
    }

    private static class PointStructureDeserializer extends StdDeserializer<ObservableList<PointStructureItem>> {
        public PointStructureDeserializer() {
            this(null);
        }

        public PointStructureDeserializer(Class vc) {
            super(vc);
        }

        @Override
        public ObservableList<PointStructureItem> deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
            JsonNode node = p.getCodec().readTree(p);
            ObservableList<PointStructureItem> pointStructure = FXCollections.observableArrayList();
            Integer index = 0;
            for (final JsonNode entry : node) {
                pointStructure.add(new PointStructureItem(index, entry.asInt()));
                index += 1;
            }
            return pointStructure;
        }
    }

    private static class PointStructureSerializer extends StdSerializer<ObservableList<PointStructureItem>> {
        public PointStructureSerializer() {
            this(null);
        }

        public PointStructureSerializer(Class<ObservableList<PointStructureItem>> t) {
            super(t);
        }

        @Override
        public void serialize(ObservableList<PointStructureItem> value, JsonGenerator gen, SerializerProvider provider) throws IOException {
            int[] pointStructure = new int[value.size()];
            Integer index = 0;
            for (PointStructureItem entry : value) {
                pointStructure[index] = entry.getPoints();
                index += 1;
            }
            gen.writeArray(pointStructure, 0, pointStructure.length);
        }
    }

    private static class ParticipantConfigurationDeserializer extends StdDeserializer<ObservableList<Driver>> {
        public ParticipantConfigurationDeserializer() {
            this(null);
        }

        public ParticipantConfigurationDeserializer(Class<?> vc) {
            super(vc);
        }

        @Override
        public ObservableList<Driver> deserialize(JsonParser p, DeserializationContext ctxt) throws IOException {
            JsonNode node = p.getCodec().readTree(p);
            ObservableList<Driver> drivers = FXCollections.observableList(new ArrayList<>(), param -> new Observable[]{param.displayNameProperty(), param.getCar().carNameProperty()});

            Iterator<Map.Entry<String, JsonNode>> iterator = node.fields();
            while (iterator.hasNext()) {
                Map.Entry<String, JsonNode> entry = iterator.next();
                Driver driver = new Driver(
                        entry.getKey(),
                        entry.getValue().findValue("display").textValue(),
                        entry.getValue().findValue("short_display").textValue(),
                        new Car(entry.getValue().findValue("car").textValue(), new CarClass("", Color.rgb(255, 0, 0))),
                        entry.getValue().findValue("team").textValue(),
                        entry.getValue().findValue("points").intValue()
                );
                drivers.add(driver);
            }

            return drivers;
        }
    }

    private static class ParticipantConfigurationSerializer extends StdSerializer<ObservableList<Driver>> {
        public ParticipantConfigurationSerializer() {
            this(null);
        }

        public ParticipantConfigurationSerializer(Class<ObservableList<Driver>> t) {
            super(t);
        }

        @Override
        public void serialize(ObservableList<Driver> value, JsonGenerator gen, SerializerProvider provider) throws IOException {
            gen.configure(JsonGenerator.Feature.ESCAPE_NON_ASCII, true);
            gen.writeStartObject();
            for (Driver driver : value.sorted(Comparator.comparing(Driver::getName))) {
                gen.writeFieldName(driver.getName());
                gen.writeStartObject();
                gen.writeStringField("display", driver.getDisplayName());
                gen.writeStringField("short_display", driver.getShortName());
                if (driver.getCar() == null) {
                    gen.writeStringField("car", null);
                } else {
                    gen.writeStringField("car", driver.getCar().getCarName());
                }
                gen.writeStringField("team", driver.getTeam());
                gen.writeNumberField("points", driver.getSeriesPoints());
                gen.writeEndObject();
            }
            gen.writeEndObject();
        }
    }
}