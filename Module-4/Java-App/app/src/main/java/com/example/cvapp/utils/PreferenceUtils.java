package com.example.cvapp.utils;

import android.content.Context;
import android.content.SharedPreferences;

public class PreferenceUtils {
    private static final String PREF_NAME = "FastNucesExplorerPrefs";
    private static final String KEY_LAST_LATITUDE = "last_latitude";
    private static final String KEY_LAST_LONGITUDE = "last_longitude";
    private static final String KEY_FOCAL_LENGTH = "focal_length";
    private static final String KEY_LAST_BUILDING = "last_building";
    private static final String KEY_LAST_BUILDING_TYPE = "last_building_type";
    private static final String KEY_SHOW_GRID = "show_grid";
    private static final String KEY_SHOW_LEGEND = "show_legend";
    private static final String KEY_SHOW_CONFIDENCE = "show_confidence";
    private static final String KEY_UPDATE_INTERVAL = "update_interval";
    private static final String KEY_FIRST_LAUNCH = "first_launch";

    private static SharedPreferences getPreferences(Context context) {
        return context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    public static void saveLastLocation(Context context, double latitude, double longitude) {
        SharedPreferences.Editor editor = getPreferences(context).edit();
        editor.putFloat(KEY_LAST_LATITUDE, (float) latitude);
        editor.putFloat(KEY_LAST_LONGITUDE, (float) longitude);
        editor.apply();
    }

    public static double[] getLastLocation(Context context) {
        SharedPreferences prefs = getPreferences(context);
        float latitude = prefs.getFloat(KEY_LAST_LATITUDE, 0f);
        float longitude = prefs.getFloat(KEY_LAST_LONGITUDE, 0f);
        return new double[]{latitude, longitude};
    }

    public static void saveFocalLength(Context context, double focalLength) {
        SharedPreferences.Editor editor = getPreferences(context).edit();
        editor.putFloat(KEY_FOCAL_LENGTH, (float) focalLength);
        editor.apply();
    }

    public static double getFocalLength(Context context) {
        return getPreferences(context).getFloat(KEY_FOCAL_LENGTH, 0f);
    }

    public static void saveLastBuilding(Context context, String buildingName, String buildingType) {
        SharedPreferences.Editor editor = getPreferences(context).edit();
        editor.putString(KEY_LAST_BUILDING, buildingName);
        editor.putString(KEY_LAST_BUILDING_TYPE, buildingType);
        editor.apply();
    }

    public static String[] getLastBuilding(Context context) {
        SharedPreferences prefs = getPreferences(context);
        String buildingName = prefs.getString(KEY_LAST_BUILDING, "");
        String buildingType = prefs.getString(KEY_LAST_BUILDING_TYPE, "");
        return new String[]{buildingName, buildingType};
    }

    public static void saveVisualizationSettings(Context context, boolean showGrid, boolean showLegend, boolean showConfidence, int updateInterval) {
        SharedPreferences.Editor editor = getPreferences(context).edit();
        editor.putBoolean(KEY_SHOW_GRID, showGrid);
        editor.putBoolean(KEY_SHOW_LEGEND, showLegend);
        editor.putBoolean(KEY_SHOW_CONFIDENCE, showConfidence);
        editor.putInt(KEY_UPDATE_INTERVAL, updateInterval);
        editor.apply();
    }

    public static boolean[] getVisualizationSettings(Context context) {
        SharedPreferences prefs = getPreferences(context);
        boolean showGrid = prefs.getBoolean(KEY_SHOW_GRID, true);
        boolean showLegend = prefs.getBoolean(KEY_SHOW_LEGEND, true);
        boolean showConfidence = prefs.getBoolean(KEY_SHOW_CONFIDENCE, true);
        return new boolean[]{showGrid, showLegend, showConfidence};
    }

    public static int getUpdateInterval(Context context) {
        return getPreferences(context).getInt(KEY_UPDATE_INTERVAL, 1000);
    }

    public static boolean isFirstLaunch(Context context) {
        return getPreferences(context).getBoolean(KEY_FIRST_LAUNCH, true);
    }

    public static void setFirstLaunch(Context context, boolean isFirst) {
        SharedPreferences.Editor editor = getPreferences(context).edit();
        editor.putBoolean(KEY_FIRST_LAUNCH, isFirst);
        editor.apply();
    }
} 