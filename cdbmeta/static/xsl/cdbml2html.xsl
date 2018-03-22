<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:c="https://www-amdis.iaea.org/cdbml">

<xsl:template match="/">
  <html>
    <body>
    <h1>CDB Record <xsl:value-of select="/c:cdbml/c:cdbrecord/@id"/></h1>

    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:attribution">
    <h2>Attribution <xsl:value-of select="@id"/></h2>
        <h3>Contributor</h3>
        <p><xsl:value-of select="c:name"/>, <xsl:value-of select="c:affiliation"/></p>
        <h3>Publication</h3>
        <p>Publication DOI:
            <xsl:element name="a">
                <xsl:attribute name="href">http://doi.org/<xsl:value-of select="c:doi"/></xsl:attribute>
            <xsl:value-of select="c:doi"/>
            </xsl:element>
        </p>

        <h3>Acknowledgements</h3>
        <p><xsl:value-of select="c:acknowledgements"/></p>
    </xsl:for-each>

    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:material">
        <h2>Material</h2>
        <p>Formula: <xsl:value-of select="c:formula"/></p>
        <p>Structure: <xsl:value-of select="c:structure"/></p>
        <xsl:apply-templates select="c:lattice_parameters"/>

    </xsl:for-each>
    <p>Simulation includes surface? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:has_surface" /></p>
    <p>Initially perfect crystal configuration? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:initially_perfect" /></p>

    <h2>PKA</h2>
    <p>PKA atomic number: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA_atomic_number" /></p>
    <p>PKA energy: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy" />&#160;<xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy/@units" /></p>
    <p>PKA by recoil? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:recoil" /></p>

    <h2>Simulation Details</h2>
    <p>Electronic stopping included? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping" /></p>
    <p>Electronic stopping comments: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping_comment" /></p>

    <p>Thermostat? <xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat" /></p>
    <p>Thermostat comments: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat_comment" /></p>

    <p>Input filename: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:input_filename" /></p>

    <p>Simulation time: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time" />&#160;<xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time/@units" /></p>

    <p>Initial temperature: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature" />&#160;<xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature/@units" /></p>

    <p>Interatomic potential filename: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:filename" /></p>
    <p>Interatomic potential comment: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:comment" /></p>

    <p>Code: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:name" /> Version: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:version" /></p>

    <h2>Data</h2>
    <p>xyz archive_name: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:archive_name" /></p>

    <h3>Columns</h3>
    <table>
    <thead><tr><th>Position</th><th>Name</th><th>Units</th></tr></thead>
    <tbody>
    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:data/c:columns/c:column">
    <tr>
        <td><xsl:value-of select="position()" /></td>
        <td><xsl:value-of select="c:name" /></td>
        <td><xsl:value-of select="c:units" /></td>
    </tr>
    </xsl:for-each>
    </tbody>
    </table>

    </body>
  </html>
</xsl:template>

<xsl:template match="c:lattice_parameters">
    <p>
        <i>a</i> = <xsl:value-of select="c:a"/>&#160;<xsl:value-of select="c:a/@units"/>,
        <i>b</i> = <xsl:value-of select="c:b"/>&#160;<xsl:value-of select="c:b/@units"/>,
        <i>c</i> = <xsl:value-of select="c:c"/>&#160;<xsl:value-of select="c:c/@units"/>.<br/>
        <i>α</i> = <xsl:value-of select="c:alpha"/><xsl:choose><xsl:when test="c:alpha/@units='deg'">°</xsl:when><xsl:otherwise>&#160;<xsl:value-of select="c:alpha/@units"/></xsl:otherwise></xsl:choose>,
        <i>β</i> = <xsl:value-of select="c:beta"/><xsl:choose><xsl:when test="c:beta/@units='deg'">°</xsl:when><xsl:otherwise>&#160;<xsl:value-of select="c:beta/@units"/></xsl:otherwise></xsl:choose>,
        <i>γ</i> = <xsl:value-of select="c:gamma"/><xsl:choose><xsl:when test="c:gamma/@units='deg'">°</xsl:when><xsl:otherwise>&#160;<xsl:value-of select="c:gamma/@units"/></xsl:otherwise></xsl:choose>,
    </p>
</xsl:template>

</xsl:stylesheet>
