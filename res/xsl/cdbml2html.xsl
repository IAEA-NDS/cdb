<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:c="https://amdis.iaea.org/cdbml">

<xsl:template match="/">
  <html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous" />
        <link rel="stylesheet" href="/static/cdbmeta/css/custom.css" />
    </head>
    <body>

<div class="container content-container">

    <h1 class="text-center">CDB Record <xsl:value-of select="/c:cdbml/c:cdbrecord/@id"/></h1>

    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:attribution">
    <div class="card">
    <div class="card-header"><h2>Attribution <xsl:value-of select="@id"/></h2></div>
    <div class="card-body">
        <h3>Contributor</h3>
        <p><xsl:value-of select="c:name"/>, <xsl:value-of select="c:affiliation"/></p>
        <h3>Publication</h3>
        <p>Publication DOI:
            <xsl:element name="a">
                <xsl:attribute name="href">https://doi.org/<xsl:value-of select="c:doi"/></xsl:attribute>
            <xsl:value-of select="c:doi"/>
            </xsl:element>
        </p>

        <h3>Acknowledgements</h3>
        <p><xsl:value-of select="c:acknowledgements"/></p>

    </div>
    </div>
    </xsl:for-each>

    <xsl:for-each select="/c:cdbml/c:cdbrecord/c:material">
        <div class="card">
        <div class="card-header"><h2>Material</h2></div>
        <div class="card-body">
        <p>Formula: <span class="value"><xsl:value-of select="c:formula"/></span></p>
        <p>Structure: <span class="value"><xsl:value-of select="c:structure"/></span></p>
        <xsl:apply-templates select="c:lattice_parameters"/>

        <p>Simulation includes surface? <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:has_surface" /></span></p>
        <p>Initially perfect crystal configuration? <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:initially_perfect" /></span></p>
        </div>
        </div>

    </xsl:for-each>

    <div class="card">
    <div class="card-header"><h2>PKA</h2></div>
    <div class="card-body">
    <p>PKA atomic number: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA_atomic_number" /></span></p>
    <p>PKA energy: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy" />&#160;<xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:energy/@units" /></span></p>
    <p>PKA by recoil? <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:PKA/c:recoil" /></span></p>
    </div>
    </div>

    <div class="card">
    <div class="card-header"><h2>Simulation Details</h2></div>
    <div class="card-body">
    <p>Electronic stopping included? <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping" /></span></p>
    <p>Electronic stopping comments: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:electronic_stopping_comment" /></span></p>

    <p>Thermostat? <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat" /></span></p>
    <p>Thermostat comments: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:thermostat_comment" /></span></p>

    <p>Input filename: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:input_filename" /></span></p>

    <p>Simulation time: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time" />&#160;<xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_time/@units" /></span></p>

    <p>Initial temperature: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature" />&#160;<xsl:value-of select="/c:cdbml/c:cdbrecord/c:initial_temperature/@units" /></span></p>

    <p>Box dimensions (Å): <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_X_length"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_Y_length"/>, <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_Z_length"/></span></p>

    <xsl:if test="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation"><p>Box orientation:
        <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:X_orientation"/>,
        <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:Y_orientation"/>,
        <xsl:value-of select="/c:cdbml/c:cdbrecord/c:simulation_box/c:box_orientation/c:Z_orientation"/>
    </p></xsl:if>

    <p>Interatomic potential URI: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:uri" /></span></p>
    <p>Interatomic potential filename: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:filename" /></span></p>
    <p>Interatomic potential comment: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:comment" /></span></p>
    <p>Interatomic potential doi: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:interatomic_potential/c:doi" /></span></p>

    <p>Code: <span class="value"><xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:name" /> Version: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:code/c:version" /></span></p>

    </div>
    </div>

    <div class="card">
    <div class="card-header"><h2>Data</h2></div>
    <div class="card-body">
    <p>Data archive name: <xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:archive_name" /></p>

    <h3>Columns</h3>
    <table class="table">
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
    </div>
    </div>

    <div class="card">
    <div class="card-header"><h2>Comments</h2></div>
    <div class="card-body">
    <pre><xsl:value-of select="/c:cdbml/c:cdbrecord/c:data/c:comments" /></pre>
    </div>
    </div>

    </div>
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
        <i>γ</i> = <xsl:value-of select="c:gamma"/><xsl:choose><xsl:when test="c:gamma/@units='deg'">°</xsl:when><xsl:otherwise>&#160;<xsl:value-of select="c:gamma/@units"/></xsl:otherwise></xsl:choose>.
    </p>
</xsl:template>

</xsl:stylesheet>
