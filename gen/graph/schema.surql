-- Graph schema generated from Fabric primitives — DO NOT EDIT BY HAND.
-- Nodes = primitives; edges = RELATION tables from each relationship.

DEFINE TABLE capability SCHEMAFULL;
DEFINE TABLE constraint SCHEMAFULL;
DEFINE TABLE event SCHEMAFULL;
DEFINE TABLE identity SCHEMAFULL;
DEFINE TABLE location SCHEMAFULL;
DEFINE TABLE objective SCHEMAFULL;
DEFINE TABLE policy SCHEMAFULL;
DEFINE TABLE relationship SCHEMAFULL;
DEFINE TABLE state SCHEMAFULL;
DEFINE TABLE thing SCHEMAFULL;
DEFINE TABLE time SCHEMAFULL;

-- Relationship edges
DEFINE TABLE heldby TYPE RELATION IN capability OUT identity;
DEFINE TABLE constrainedby TYPE RELATION IN capability OUT constraint;
DEFINE TABLE governedby TYPE RELATION IN capability OUT policy;
DEFINE TABLE servesobjective TYPE RELATION IN capability OUT objective;
DEFINE TABLE composesinto TYPE RELATION IN constraint OUT policy;
DEFINE TABLE limits TYPE RELATION IN constraint OUT capability;
DEFINE TABLE records TYPE RELATION IN event OUT capability;
DEFINE TABLE triggers TYPE RELATION IN event OUT state;
DEFINE TABLE holds TYPE RELATION IN identity OUT capability;
DEFINE TABLE subjectto TYPE RELATION IN identity OUT policy;
DEFINE TABLE locatedat TYPE RELATION IN identity OUT location;
DEFINE TABLE bounds TYPE RELATION IN location OUT constraint;
DEFINE TABLE servedby TYPE RELATION IN objective OUT capability;
DEFINE TABLE boundedby TYPE RELATION IN objective OUT constraint;
DEFINE TABLE measuredby TYPE RELATION IN objective OUT event;
DEFINE TABLE subobjectiveof TYPE RELATION IN objective OUT objective;
DEFINE TABLE composedof TYPE RELATION IN policy OUT constraint;
DEFINE TABLE governs TYPE RELATION IN policy OUT capability;
DEFINE TABLE appliesto TYPE RELATION IN policy OUT identity;
DEFINE TABLE connects TYPE RELATION IN relationship OUT thing;
DEFINE TABLE advancedby TYPE RELATION IN state OUT event;
DEFINE TABLE gatedby TYPE RELATION IN state OUT constraint;
DEFINE TABLE relatedto TYPE RELATION IN thing OUT thing;
DEFINE TABLE scopes TYPE RELATION IN time OUT constraint;
