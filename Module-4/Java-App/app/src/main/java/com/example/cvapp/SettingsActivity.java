package com.example.cvapp;

import android.os.Bundle;
import android.view.MenuItem;
import android.widget.CompoundButton;

import androidx.appcompat.app.AppCompatActivity;

import com.example.cvapp.databinding.ActivitySettingsBinding;
import com.example.cvapp.utils.PreferenceUtils;
import com.example.cvapp.utils.UIUtils;

public class SettingsActivity extends AppCompatActivity {
    private ActivitySettingsBinding binding;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivitySettingsBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        setupToolbar();
        loadSettings();
        setupListeners();
    }

    private void setupToolbar() {
        setSupportActionBar(binding.toolbar);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);
        getSupportActionBar().setTitle(R.string.settings);
    }

    private void loadSettings() {
        boolean[] visualizationSettings = PreferenceUtils.getVisualizationSettings(this);
        binding.showGridSwitch.setChecked(visualizationSettings[0]);
        binding.showLegendSwitch.setChecked(visualizationSettings[1]);
        binding.showConfidenceSwitch.setChecked(visualizationSettings[2]);

        int updateInterval = PreferenceUtils.getUpdateInterval(this);
        binding.updateIntervalSlider.setValue(updateInterval);
        binding.updateIntervalText.setText(getString(R.string.update_interval_ms, updateInterval));
    }

    private void setupListeners() {
        binding.showGridSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> saveSettings());
        binding.showLegendSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> saveSettings());
        binding.showConfidenceSwitch.setOnCheckedChangeListener((buttonView, isChecked) -> saveSettings());

        binding.updateIntervalSlider.addOnChangeListener((slider, value, fromUser) -> {
            int interval = (int) value;
            binding.updateIntervalText.setText(getString(R.string.update_interval_ms, interval));
            if (fromUser) {
                saveSettings();
            }
        });
    }

    private void saveSettings() {
        boolean showGrid = binding.showGridSwitch.isChecked();
        boolean showLegend = binding.showLegendSwitch.isChecked();
        boolean showConfidence = binding.showConfidenceSwitch.isChecked();
        int updateInterval = (int) binding.updateIntervalSlider.getValue();

        PreferenceUtils.saveVisualizationSettings(this, showGrid, showLegend, showConfidence, updateInterval);
        UIUtils.showToast(this, getString(R.string.settings_saved));
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            onBackPressed();
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
} 