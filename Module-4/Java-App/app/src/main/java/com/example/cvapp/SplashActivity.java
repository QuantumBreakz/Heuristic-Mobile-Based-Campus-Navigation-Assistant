package com.example.cvapp;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;

import androidx.appcompat.app.AppCompatActivity;

import com.airbnb.lottie.LottieAnimationView;
import com.example.cvapp.utils.PreferenceUtils;

public class SplashActivity extends AppCompatActivity {
    private static final long SPLASH_DELAY = 2000; // 2 seconds

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_splash);

        LottieAnimationView splashAnimation = findViewById(R.id.splashAnimation);
        splashAnimation.setAnimation(R.raw.splash_animation);
        splashAnimation.playAnimation();

        // Check if this is the first launch
        boolean isFirstLaunch = PreferenceUtils.isFirstLaunch(this);
        if (isFirstLaunch) {
            // Show welcome animation for first launch
            splashAnimation.setAnimation(R.raw.welcome_animation);
            splashAnimation.playAnimation();
            PreferenceUtils.setFirstLaunch(this, false);
        }

        // Navigate to MainActivity after delay
        new Handler(Looper.getMainLooper()).postDelayed(() -> {
            startActivity(new Intent(SplashActivity.this, MainActivity.class));
            finish();
            overridePendingTransition(R.anim.fade_in, R.anim.fade_out);
        }, SPLASH_DELAY);
    }
} 