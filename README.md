# IOS-XR-XML

This Python program will send two XML query to IOS XR BNG router against mac-addresses for IPoE sessions.
First to get the session detail and other one two get the subscriber interface statistics.

Library Used in program.

    argparse
    xml.etree.ElementTree 
    telnetlib
    time
    netaddr

<b>Sample Output</b>:

<table width="200" border="1">
<tbody>
  <tr>
    <td><table width="500" height="240" border="3">
      <tbody>
        <tr>
          <th width="103" scope="col">Mac Address</th>
          <th width="127" scope="col">Subscriber Interface</th>
          <th width="231" scope="col">Elapsed Time</th>
        </tr>
        <tr>
          <td>0000.6602.01de</td>
          <td>Bundle-Ether1.200.ip30226</td>
          <td>0.00413393974304</td>
        </tr>
        <tr>
          <td>0000.6602.01df</td>
          <td>Bundle-Ether1.200.ip30227</td>
          <td>0.00372815132141</td>
        </tr>
        <tr>
          <td>0000.6602.01e0</td>
          <td>Bundle-Ether1.200.ip30228</td>
          <td>0.00392985343933</td>
        </tr>
      </tbody>
    </table></td>
  </tr>
</tbody>
