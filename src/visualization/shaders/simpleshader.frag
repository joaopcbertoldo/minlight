uniform vec4 light_position;
uniform vec4 light_direction;
uniform float light_radius;

varying vec4 out_Color;
varying vec4 position;
varying vec4 out_Normal;

void main()
{
	// vector from the point to the light source
	vec4 pq = light_position - position;
	
	//checks if the point is illuminated by the sun
	if( gl_FrontFacing && dot(light_direction,out_Normal) < 0.0  && length(cross(pq.xyz,light_direction.xyz)) / length(light_direction.xyz) < light_radius)
	{
		//if the point is illuminated, the color is stronger
		gl_FragColor = out_Color*1.2; 
	}
	else
	{
		//FrontFacing test to check which face of the triangle the camera is looking at
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
}
