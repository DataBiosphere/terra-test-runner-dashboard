import "bootstrap/dist/css/bootstrap.min.css";
import Color from "color";
import React, {useState} from "react";
import PropTypes from "prop-types";

/**
 * A function component that implements flex tab bar
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
export const FlexTabBar = (props) => {
    const [flexDirection, setflexDirection] = useState("column");

    return (
        <PreviewLayout
            label="flexDirection"
            values={[
                "Buffer Services",
                "External Credentials",
                "Workspace Manager",
                "MC Terra Service 1",
                "MC Terra Service 2",
                "MC Terra Service 3",
                "MC Terra Service 4",
                "MC Terra Service 5",
                "MC Terra Service 6",
                "MC Terra Service 7",
                "MC Terra Service 8",
                "MC Terra Service 9",
                "BVDP"
            ]}
            selectedValue={flexDirection}
            setSelectedValue={setflexDirection}
        >
            <div style={{...styles.box, ...{backgroundColor: "#74ae43"}}}/>
            <div style={{...styles.box, ...{backgroundColor: "#c02f42"}}}/>
            <div style={{...styles.box, ...{backgroundColor: "#e0dd10"}}}/>
            <div style={{...styles.box, ...{backgroundColor: "#005f6f"}}}/>
            <div style={{...styles.box, ...{backgroundColor: "#c41061"}}}/>
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
    <div style={{padding: 10, flex: 1}}>
        <div className="d-flex flex-row flex-wrap mb-3">
            {values.map((value) => (
                <div
                    key={value}
                    onClick={() => setSelectedValue(value)}
                    style={{
                        ...styles.button,
                        ...{
                            backgroundColor:
                                selectedValue === value
                                    ? "#74ae43"
                                    : styles.button.backgroundColor,
                            borderWidth: 0
                        }
                    }}
                >
                    <div
                        style={{
                            ...styles.buttonLabel,
                            ...{
                                color:
                                    selectedValue === value
                                        ? styles.selectedLabel.color
                                        : styles.buttonLabel.color
                            }
                        }}
                        className="p-2"
                    >
                        {value}
                    </div>
                </div>
            ))}
        </div>
        <div
            style={{...styles.container, ...{[label]: "row"}}}
            className="d-flex flex-row flex-wrap mb-3"
        >
            {children}
        </div>
    </div>
);

const styles = {
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
        margin: 1,
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
};

FlexTabBar.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string
}
