package com.senorpez.projectcars.replayenhancer;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

abstract class Packet {
    private final Integer buildVersionNumber;

    Packet(ByteBuffer data) {
        this.buildVersionNumber = ReadUnsignedShort(data);
    }

    private static byte[] ReadBytes(ByteBuffer data, int length) {
        byte[] readBytes = new byte[length];
        data.get(readBytes);
        return readBytes;
    }

    private static Integer GetUnsigned(ByteBuffer data, int length) {
        Integer returnValue = 0;
        for (byte chunk : ReadBytes(data, length)) {
            returnValue <<= 8;
            returnValue |= (int)chunk & 0xFF;
        }
        return returnValue;
    }

    Integer getBuildVersionNumber() {
        return buildVersionNumber;
    }

    abstract Short getPacketType();

    abstract Short getCount();

    static Short getPacketType(Short packetType) {
        Integer mask = 3; /* 0000 0011 */
        return Integer.valueOf(mask & packetType).shortValue();
    }

    static Short getCount(Short packetType) {
        return packetType >>> 2;
    }

    static Short ReadUnsignedByte(ByteBuffer data) {
        return GetUnsigned(data, 1).shortValue();
    }

    static Integer ReadUnsignedShort(ByteBuffer data) {
        return GetUnsigned(data, 2);
    }

    static Byte ReadSignedByte(ByteBuffer data) {
        return ByteBuffer.wrap(ReadBytes(data, 1)).get();
    }

    static Short ReadSignedShort(ByteBuffer data) {
        return ByteBuffer.wrap(ReadBytes(data, 2)).getShort();
    }

    static Float ReadFloat(ByteBuffer data) {
        return ByteBuffer.wrap(ReadBytes(data, 4)).getFloat();
    }

    static String ReadString(ByteBuffer data) {
        return new String(ReadBytes(data, 64), StandardCharsets.UTF_8).split("\u0000", 2)[0];
    }
}
