package com.example.cvapp.utils;

import android.content.Context;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Toast;

import com.google.android.material.snackbar.Snackbar;

public class UIUtils {
    public static void showToast(Context context, String message) {
        Toast.makeText(context, message, Toast.LENGTH_SHORT).show();
    }

    public static void showLongToast(Context context, String message) {
        Toast.makeText(context, message, Toast.LENGTH_LONG).show();
    }

    public static void showSnackbar(View view, String message) {
        Snackbar.make(view, message, Snackbar.LENGTH_SHORT).show();
    }

    public static void showSnackbarWithAction(View view, String message, String actionText, View.OnClickListener listener) {
        Snackbar.make(view, message, Snackbar.LENGTH_LONG)
                .setAction(actionText, listener)
                .show();
    }

    public static void fadeIn(View view, Context context) {
        Animation fadeIn = AnimationUtils.loadAnimation(context, android.R.anim.fade_in);
        view.startAnimation(fadeIn);
        view.setVisibility(View.VISIBLE);
    }

    public static void fadeOut(View view, Context context) {
        Animation fadeOut = AnimationUtils.loadAnimation(context, android.R.anim.fade_out);
        view.startAnimation(fadeOut);
        view.setVisibility(View.GONE);
    }

    public static void slideIn(View view, Context context) {
        Animation slideIn = AnimationUtils.loadAnimation(context, android.R.anim.slide_in_left);
        view.startAnimation(slideIn);
        view.setVisibility(View.VISIBLE);
    }

    public static void slideOut(View view, Context context) {
        Animation slideOut = AnimationUtils.loadAnimation(context, android.R.anim.slide_out_right);
        view.startAnimation(slideOut);
        view.setVisibility(View.GONE);
    }

    public static void setViewEnabled(View view, boolean enabled) {
        view.setEnabled(enabled);
        view.setAlpha(enabled ? 1.0f : 0.5f);
    }

    public static void setViewsEnabled(boolean enabled, View... views) {
        for (View view : views) {
            setViewEnabled(view, enabled);
        }
    }
} 