package bartoszgorka.rest;

import bartoszgorka.models.Course;
import bartoszgorka.storage.DB;

import javax.annotation.security.RolesAllowed;
import javax.ws.rs.*;
import javax.ws.rs.core.*;
import java.util.Set;

@Path("/courses")
public class CoursesREST {
    @GET
    @Produces({MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML})
    public Set<Course> getAllCourses() {
        for (Course c : DB.getCourses()) {
            c.clearLinks();
        }
        return DB.getCourses();
    }

    @POST
    @Consumes({MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML})
    @Produces({MediaType.APPLICATION_JSON, MediaType.APPLICATION_XML})
    @RolesAllowed({"supervisor", "admin"})
    public Response registerNewCourse(Course rawCourseBody, @Context UriInfo uriInfo) throws BadRequestException {
        Course newCourse = DB.registerNewCourse(rawCourseBody);
        newCourse.clearLinks();

        UriBuilder builder = uriInfo.getAbsolutePathBuilder();
        builder.path(Integer.toString(newCourse.getID()));
        return Response.created(builder.build()).entity(newCourse).build();
    }
}