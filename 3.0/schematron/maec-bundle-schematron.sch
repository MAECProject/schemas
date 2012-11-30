<?xml version="1.0" encoding="UTF-8"?>
<!--MAEC v2.1 schematron validation rules
    Currently, these only apply to MAEC Actions and Objects-->
<sch:schema xmlns:sch="http://purl.oclc.org/dsdl/schematron" queryBinding="xslt2">
    <sch:ns prefix="maecBundle" uri="http://maec.mitre.org/XMLSchema/maec-bundle-3"/>
    <sch:pattern id="actionIDpattern">
        <sch:rule context="/*//maecBundle:Action">
            <sch:assert test="matches(@id, '^maec-[A-Za-z0-9_\-\.]+-act-[1-9][0-9]*$')">The Action id attribute is required and must follow the correct syntax. A dash-delimited format is used with the id or idref starting with the word maec followed by a unique string, followed by the three letter code 'act', and ending with an integer.</sch:assert>
        </sch:rule>
    </sch:pattern>
    <sch:pattern id="actionRefpattern">
        <sch:rule context="/*//maecBundle:Action_Reference">
            <sch:assert test="matches(@action_id, '^maec-[A-Za-z0-9_\-\.]+-act-[1-9][0-9]*$')">The Action_Reference action_id attribute is required and must follow the correct syntax. A dash-delimited format is used with the id or idref starting with the word maec followed by a unique string, followed by the three letter code 'act', and ending with an integer.</sch:assert>
        </sch:rule>
    </sch:pattern>
    <sch:pattern id="actionIDREFpattern">
        <sch:rule context="/*//maecBundle:Action">
            <sch:assert test="not(@idref)">A MAEC action must not have an idref attribute. To reference an action, the CybOX ActionReferenceType must be used.</sch:assert>
        </sch:rule>
    </sch:pattern>
    <sch:pattern id="objectIDREFpattern">
        <sch:rule context="/*//maecBundle:Object">
            <sch:assert test="not(@idref)">A MAEC object must not have an idref attribute. To reference an object, the MAEC Bundle ObjectReferenceType must be used.</sch:assert>
        </sch:rule>
    </sch:pattern>
</sch:schema>