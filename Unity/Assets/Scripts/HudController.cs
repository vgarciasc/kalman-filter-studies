using System.Collections;
using System.Collections.Generic;
using UnityEngine.UI;
using UnityEngine;

public class HudController : MonoBehaviour {

	[SerializeField]
	GameObject settingsMenu;

	public Sensor GPS, IMU;
	public Image recording;

	void Start () {
		ToggleRecording(false);
		GPS.RecordEvent += ToggleRecording;
		IMU.RecordEvent += ToggleRecording;
	}

	void ToggleRecording(bool value) {
		recording.color = value ? Color.red : Color.grey; 
	}

	public void ToggleSettingsMenu() {
		settingsMenu.SetActive(!settingsMenu.activeSelf);
	}
}
