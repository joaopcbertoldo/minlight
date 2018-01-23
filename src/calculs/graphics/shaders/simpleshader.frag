uniform vec4 light_position;
uniform vec4 light_direction;
uniform float light_radius;

varying vec4 out_Color;
varying vec4 position;
varying vec4 out_Normal;

void main()
{
	vec4 pq = light_position - position;

	if( gl_FrontFacing && dot(light_direction,out_Normal) < 0.0  && length(cross(pq.xyz,light_direction.xyz)) / length(light_direction.xyz) < light_radius)
	{
		gl_FragColor = out_Color*1.2;
	}
	else
	{
		if(gl_FrontFacing )
		{
			gl_FragColor = out_Color;
		}
		else
		{
			gl_FragColor.xyz = 0.5*out_Color.xyz;
			gl_FragColor.w = out_Color.w;
		}
}
	//gl_FragColor = out_Normal;
}
