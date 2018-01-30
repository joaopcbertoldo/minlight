varying vec4 out_Color;
varying vec4 position;
varying vec4 out_Normal;

//MUST USE GLNORMAL AND GL_NORMAL TO LIGHTING
//for light source + direction, must use uniform
//for the back face thing, maybe add triangles inside to make it easier?
//to avoid light behind the source, use parameters just like ray tracing


void main()
{
	vec4 p;
	p.xyz = gl_Vertex.xyz;
  p.w = 1.0;

	out_Normal.xyz = gl_Normal.xyz;
	out_Normal.w = 0.0;

  position = p;

  out_Color = gl_Color;
  gl_Position = gl_ModelViewProjectionMatrix*gl_Vertex;
	gl_ModelViewProjectionMatrix * p;
}
