import Color from "color";
import React, { useState } from "react";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";
import PropTypes from "prop-types";

/**
 * A function component that renders a tab bar.
 * @returns {JSX.Element}
 * @constructor
 */
const TabBar = (props) => {
  const [flexDirection, setflexDirection] = useState("column");

  return (
    <PreviewLayout
      label="flexDirection"
      values={[
        "Buffer Services",
        "External Credentials",
        "Workspace Manager",
        "BVDP"
      ]}
      selectedValue={flexDirection}
      setSelectedValue={setflexDirection}
    >
      <View style={[styles.box, { backgroundColor: "#74ae43" }]} />
      <View style={[styles.box, { backgroundColor: "#c02f42" }]} />
      <View style={[styles.box, { backgroundColor: "#e0dd10" }]} />
      <View style={[styles.box, { backgroundColor: "#005f6f" }]} />
      <View style={[styles.box, { backgroundColor: "#c41061" }]} />
    </PreviewLayout>
  );
};

const PreviewLayout = ({
  label,
  children,
  values,
  selectedValue,
  setSelectedValue
}) => (
  <View style={{ padding: 10, flex: 1 }}>
    <Text style={styles.label}>{label}</Text>
    <View style={styles.row}>
      {values.map((value) => (
        <TouchableOpacity
          key={value}
          onPress={() => setSelectedValue(value)}
          style={[styles.button, selectedValue === value && styles.selected]}
        >
          <Text
            style={[
              styles.buttonLabel,
              selectedValue === value && styles.selectedLabel
            ]}
          >
            {value}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
    <View style={[styles.container, { [label]: "row" }]}>{children}</View>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
    marginTop: 8,
    backgroundColor: "aliceblue"
  },
  box: {
    width: 50,
    height: 50
  },
  row: {
    flexDirection: "row",
    flexWrap: "wrap"
  },
  button: {
    paddingHorizontal: 20,
    paddingVertical: 18,
    borderRadius: 2,
    backgroundColor: Color("#74ae43").mix(Color("white"), 0.4).hex(),
    alignSelf: "flex-start",
    marginHorizontal: 1,
    marginBottom: 1,
    minWidth: "10%",
    textAlign: "center"
  },
  selected: {
    backgroundColor: "#74ae43",
    borderWidth: 0
  },
  buttonLabel: {
    fontSize: 18,
    fontWeight: "500",
    color: "white"
  },
  selectedLabel: {
    color: "white"
  },
  label: {
    textAlign: "center",
    marginBottom: 10,
    fontSize: 24
  }
});

TabBar.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string
}

export default TabBar;
